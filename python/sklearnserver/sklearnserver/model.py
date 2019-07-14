# Copyright 2019 kubeflow.org.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import kfserving
import joblib
import pickle
import numpy as np
import os
from typing import List

JOBLIB_FILE = "model.joblib"

class SKLearnModel(kfserving.KFModel): #pylint:disable=c-extension-no-member
    def __init__(self, name: str, model_dir: str):
        super().__init__(name)
        self.name = name
        self.model_dir = model_dir
        self.model_file = JOBLIB_FILE
        self.ready = False

    def load(self):
        model_file = os.path.join(kfserving.Storage.download(self.model_dir), self.model_file) #pylint:disable=c-extension-no-member
        try:
            self._joblib = joblib.load(model_file) #pylint:disable=attribute-defined-outside-init
        except:
            logging.warn("Unable to deserialize with joblib... tyring pickle")
            with open(model_file.replace('.joblib', '.pkl'), 'rb') as handle:
                self._joblib = pickle.load(handle)
        self.ready = True

    def predict(self, body: List) -> List:
        try:
            inputs = np.array(body)
        except Exception as e:
            raise Exception(
                "Failed to initialize NumPy array from inputs: %s, %s" % (e, inputs))
        try:
            result = self._joblib.predict(inputs).tolist()
            return result
        except Exception as e:
            raise Exception("Failed to predict %s" % e)
