
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV


class LogisticRegressionWithThreshold:
	"""
	A modified Logistic Regression classifier that will filter calls by a custom threshold, instead of the default 0.5. This allows for control of the precision-recall tradeoff, e.g. false positives versus false negatives.
	
	:ivar clf: The underlying LogisticRegression classifier
	:ivar threshold: Threshold to use, should be between 0 and 1
	"""

	def __init__(self,threshold=0.5):
		"""
		Set up a Logistic Regression classifier that can use a different threshold for predictions and thereby be more lenient (lower threshold, false positives increase, false negatives decrease) or more conservative (higher threshold, false positives decrease, false negative increase).
		
		:param threshold: Threshold to use, should be between 0 and 1
		:type threshold: float
		"""
		
		assert threshold >= 0 and threshold <= 1, "Threshold must be between 0 and 1"

		model_params = {
			"C": [0.00390625, 0.5, 4],
		}

		clf = LogisticRegression(
			class_weight=None, random_state=1, solver='liblinear', multi_class='ovr', tol=1e-3
		)
		self.clf = GridSearchCV(clf, model_params, cv=3, scoring="f1_micro")
		self.threshold = threshold

	def fit(self,X,Y):
		"""
		Train the classifier using the associated matrix X and classes Y. Class zero should represent no associated class.
		
		:param X: Training vector
		:param Y: Associated class for each row of X
		:type X: sparse matrix
		:type Y: matrix
		"""

		self.clf.fit(X,Y)
		self.classes_ = self.clf.classes_

	def predict(self,X):
		"""
		Make predictions for the class of each row in X. Class zero should represent no prediction.
		
		:param X: Testing vector
		:type X: sparse matrix
		:return: Predictions of classes for each row in X
		:rtype: matrix
		"""

		# probs = self.clf.predict_proba(X)
		probs = self.clf.best_estimator_.predict_proba(X)

		# Ignore probabilities that fall below our threshold
		probs[probs<self.threshold] = -1.0

		# Make sure that the zero class is only select if all other options are below the threshold
		probs[:,0] = -0.5

		# And get the highest probability for each row
		predictions = np.argmax(probs,axis=1)

		return predictions

	def predict_proba(self,X):
		"""
		Calculate probabilities for the class of each row in X. Class zero should represent no prediction.
		Returns a matrix of probabilities
		
		:param X: Testing vector
		:type X: sparse matrix
		:return: Probabilities of classes for each row in X
		:rtype: matrix
		"""

		return self.clf.best_estimator_.predict_proba(X)
