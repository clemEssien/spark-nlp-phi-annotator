# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.text_annotation import TextAnnotation
from openapi_server.models.text_location_annotation_all_of import TextLocationAnnotationAllOf
from openapi_server import util

from openapi_server.models.text_annotation import TextAnnotation  # noqa: E501
from openapi_server.models.text_location_annotation_all_of import TextLocationAnnotationAllOf  # noqa: E501

class TextLocationAnnotation(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, start=None, length=None, text=None, confidence=None, location_type=None):  # noqa: E501
        """TextLocationAnnotation - a model defined in OpenAPI

        :param start: The start of this TextLocationAnnotation.  # noqa: E501
        :type start: int
        :param length: The length of this TextLocationAnnotation.  # noqa: E501
        :type length: int
        :param text: The text of this TextLocationAnnotation.  # noqa: E501
        :type text: str
        :param confidence: The confidence of this TextLocationAnnotation.  # noqa: E501
        :type confidence: float
        :param location_type: The location_type of this TextLocationAnnotation.  # noqa: E501
        :type location_type: str
        """
        self.openapi_types = {
            'start': int,
            'length': int,
            'text': str,
            'confidence': float,
            'location_type': str
        }

        self.attribute_map = {
            'start': 'start',
            'length': 'length',
            'text': 'text',
            'confidence': 'confidence',
            'location_type': 'locationType'
        }

        self._start = start
        self._length = length
        self._text = text
        self._confidence = confidence
        self._location_type = location_type

    @classmethod
    def from_dict(cls, dikt) -> 'TextLocationAnnotation':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The TextLocationAnnotation of this TextLocationAnnotation.  # noqa: E501
        :rtype: TextLocationAnnotation
        """
        return util.deserialize_model(dikt, cls)

    @property
    def start(self):
        """Gets the start of this TextLocationAnnotation.

        The position of the first character  # noqa: E501

        :return: The start of this TextLocationAnnotation.
        :rtype: int
        """
        return self._start

    @start.setter
    def start(self, start):
        """Sets the start of this TextLocationAnnotation.

        The position of the first character  # noqa: E501

        :param start: The start of this TextLocationAnnotation.
        :type start: int
        """
        if start is None:
            raise ValueError("Invalid value for `start`, must not be `None`")  # noqa: E501

        self._start = start

    @property
    def length(self):
        """Gets the length of this TextLocationAnnotation.

        The length of the annotation  # noqa: E501

        :return: The length of this TextLocationAnnotation.
        :rtype: int
        """
        return self._length

    @length.setter
    def length(self, length):
        """Sets the length of this TextLocationAnnotation.

        The length of the annotation  # noqa: E501

        :param length: The length of this TextLocationAnnotation.
        :type length: int
        """
        if length is None:
            raise ValueError("Invalid value for `length`, must not be `None`")  # noqa: E501

        self._length = length

    @property
    def text(self):
        """Gets the text of this TextLocationAnnotation.

        The string annotated  # noqa: E501

        :return: The text of this TextLocationAnnotation.
        :rtype: str
        """
        return self._text

    @text.setter
    def text(self, text):
        """Sets the text of this TextLocationAnnotation.

        The string annotated  # noqa: E501

        :param text: The text of this TextLocationAnnotation.
        :type text: str
        """
        if text is None:
            raise ValueError("Invalid value for `text`, must not be `None`")  # noqa: E501

        self._text = text

    @property
    def confidence(self):
        """Gets the confidence of this TextLocationAnnotation.

        The confidence in the accuracy of the annotation  # noqa: E501

        :return: The confidence of this TextLocationAnnotation.
        :rtype: float
        """
        return self._confidence

    @confidence.setter
    def confidence(self, confidence):
        """Sets the confidence of this TextLocationAnnotation.

        The confidence in the accuracy of the annotation  # noqa: E501

        :param confidence: The confidence of this TextLocationAnnotation.
        :type confidence: float
        """
        if confidence is None:
            raise ValueError("Invalid value for `confidence`, must not be `None`")  # noqa: E501
        if confidence is not None and confidence > 100:  # noqa: E501
            raise ValueError("Invalid value for `confidence`, must be a value less than or equal to `100`")  # noqa: E501
        if confidence is not None and confidence < 0:  # noqa: E501
            raise ValueError("Invalid value for `confidence`, must be a value greater than or equal to `0`")  # noqa: E501

        self._confidence = confidence

    @property
    def location_type(self):
        """Gets the location_type of this TextLocationAnnotation.

        Type of location  # noqa: E501

        :return: The location_type of this TextLocationAnnotation.
        :rtype: str
        """
        return self._location_type

    @location_type.setter
    def location_type(self, location_type):
        """Sets the location_type of this TextLocationAnnotation.

        Type of location  # noqa: E501

        :param location_type: The location_type of this TextLocationAnnotation.
        :type location_type: str
        """
        allowed_values = ["city", "country", "department", "hospital", "organization", "other", "room", "state", "street", "zip"]  # noqa: E501
        if location_type not in allowed_values:
            raise ValueError(
                "Invalid value for `location_type` ({0}), must be one of {1}"
                .format(location_type, allowed_values)
            )

        self._location_type = location_type
