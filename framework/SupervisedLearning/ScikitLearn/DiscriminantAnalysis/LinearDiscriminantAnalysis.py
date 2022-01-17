# Copyright 2017 Battelle Energy Alliance, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
  Created on Jan 21, 2020

  @author: alfoa, wangc
  LinearDiscriminantAnalysis
  Classifier implementing Discriminant Analysis (Linear) classification

"""
#Internal Modules (Lazy Importer)--------------------------------------------------------------------
#Internal Modules (Lazy Importer) End----------------------------------------------------------------

#External Modules------------------------------------------------------------------------------------
#External Modules End--------------------------------------------------------------------------------

#Internal Modules------------------------------------------------------------------------------------
from SupervisedLearning.ScikitLearn import ScikitLearnBase
from utils import InputData, InputTypes
#Internal Modules End--------------------------------------------------------------------------------

class LinearDiscriminantAnalysisClassifier(ScikitLearnBase):
  """
    KNeighborsClassifier
    Classifier implementing the k-nearest neighbors vote.
  """
  info = {'problemtype':'classification', 'normalize':False}

  def __init__(self):
    """
      Constructor that will appropriately initialize a supervised learning object
      @ In, None
      @ Out, None
    """
    super().__init__()
    import sklearn
    import sklearn.discriminant_analysis
    self.model = sklearn.discriminant_analysis.LinearDiscriminantAnalysis

  @classmethod
  def getInputSpecification(cls):
    """
      Method to get a reference to a class that specifies the input data for
      class cls.
      @ In, cls, the class for which we are retrieving the specification
      @ Out, inputSpecification, InputData.ParameterInput, class to use for
        specifying input of cls.
    """
    specs = super(LinearDiscriminantAnalysisClassifier, cls).getInputSpecification()
    specs.description = r"""The \xmlNode{LinearDiscriminantAnalysisClassifier} is a classifier with a linear decision boundary,
    generated by fitting class conditional densities to the data and using Bayes' rule.
    The model fits a Gaussian density to each class, assuming that all classes share the same covariance matrix.
    The fitted model can also be used to reduce the dimensionality of the input by projecting it to the most discriminative
    directions, using the transform method.
    \zNormalizationNotPerformed{LinearDiscriminantAnalysisClassifier}
    """
    specs.addSub(InputData.parameterInputFactory("solver", contentType=InputTypes.StringType,
                                                 descr=r"""Solver to use, possible values:
                                                 \begin{itemize}
                                                   \item svd: Singular value decomposition (default). Does not compute the covariance matrix,
                                                               therefore this solver is recommended for data with a large number of features.
                                                   \item lsqr: Least squares solution. Can be combined with shrinkage or custom covariance estimator.
                                                   \item eigen: Eigenvalue decomposition. Can be combined with shrinkage or custom covariance estimator.
                                                 \end{itemize}
                                                 """, default='svd'))
    specs.addSub(InputData.parameterInputFactory("Shrinkage", contentType=InputTypes.FloatOrStringType,
                                                 descr=r"""Shrinkage parameter, possible values: 1) None: no shrinkage (default),
                                                 2) `auto': automatic shrinkage using the Ledoit-Wolf lemma,
                                                 3) float between 0 an d1: fixed shrinkage parameter.
                                                 This should be left to None if covariance_estimator is used. Note that shrinkage works
                                                 only with `lsqr' and `eigen' solvers.""", default=None))
    specs.addSub(InputData.parameterInputFactory("priors", contentType=InputTypes.FloatListType,
                                                 descr=r"""The class prior probabilities. By default, the class proportions are inferred from the training data.""", default=None))
    specs.addSub(InputData.parameterInputFactory("n_components", contentType=InputTypes.IntegerType,
                                                 descr=r"""Number of components (<= min(n\_classes - 1, n\_features)) for dimensionality reduction.
                                                 If None, will be set to min(n\_classes - 1, n\_features). This parameter only affects the transform
                                                 method.""", default=None))
    specs.addSub(InputData.parameterInputFactory("store_covariance", contentType=InputTypes.BoolType,
                                                 descr=r"""If True, explicitely compute the weighted within-class covariance matrix when solver
                                                 is `svd'. The matrix is always computed and stored for the other solvers.""", default=False))
    specs.addSub(InputData.parameterInputFactory("tol", contentType=InputTypes.FloatType,
                                                 descr=r"""Absolute threshold for a singular value of X to be considered significant, used to estimate the rank of X.
                                                 Dimensions whose singular values are non-significant are discarded. Only used if solver is `svd'.""", default=1.0e-4))
    specs.addSub(InputData.parameterInputFactory("covariance_estimator", contentType=InputTypes.IntegerType,
                                                 descr=r"""covariance estimator (not supported)""", default=None))
    return specs

  def _handleInput(self, paramInput):
    """
      Function to handle the common parts of the distribution parameter input.
      @ In, paramInput, ParameterInput, the already parsed input.
      @ Out, None
    """
    super()._handleInput(paramInput)
    settings, notFound = paramInput.findNodesAndExtractValues(['solver', 'Shrinkage', 'priors',
                                                               'n_components', 'store_covariance','tol', 'covariance_estimator'])
    # notFound must be empty
    assert(not notFound)
    self.initializeModel(settings)
