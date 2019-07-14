image_name=ehallmark1122/kfserving-model-initializer
image_tag=master
full_image_name=${image_name}:${image_tag}

cd "$(dirname "$0")"

docker build -t "$full_image_name" -f model-initializer.Dockerfile .
echo "Build successful"
echo "Logging on to docker"
docker login
echo "Logged in"
docker push "$full_image_name"
echo "Pushed successful"

#Output the strict image name (which contains the sha256 image digest)
#This name can be used by the subsequent steps to refer to the exact image that was built even if another image with the same name was pushed.
image_name_with_digest=$(docker inspect --format="{{index .RepoDigests 0}}" "$image_name")
echo $image_name_with_digest
