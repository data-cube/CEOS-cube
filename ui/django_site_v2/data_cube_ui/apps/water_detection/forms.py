# Copyright 2016 United States Government as represented by the Administrator
# of the National Aeronautics and Space Administration. All Rights Reserved.
#
# Portion of this code is Copyright Geoscience Australia, Licensed under the
# Apache License, Version 2.0 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of the License
# at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# The CEOS 2 platform is licensed under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django import forms

import datetime

from .models import AnimationType, ResultType

"""
File designed to house the different forms for taking in user input in the web application.  Forms
allow for input validation and passing of data.  Includes forms for creating Queries to be ran.
"""

# Author: AHDS
# Creation date: 2016-06-23
# Modified by:
# Last modified date:

years_range = list(range(1990, datetime.datetime.now().year + 1))


class DataSelectForm(forms.Form):
    """
    Django form to be created for selecting information and validating input for:
        result_type
        animated_product
        title
        description
    """

    # these are done in the init funct.
    result_type = forms.ChoiceField(
        label='Image Background Color:', widget=forms.Select(attrs={'class': 'field-long'}))

    animation_list = [(animation_type.type_id, animation_type.type_name)
                            for animation_type in AnimationType.objects.all()]
    animated_product = forms.ChoiceField(label='Generate Time Series Animation', widget=forms.Select(
        attrs={'class': 'field-long tooltipped'}), choices=animation_list, help_text='Generate a .gif containing water extents for every scene. Use the output tab to download this result.')
    title = forms.CharField(widget=forms.HiddenInput())
    description = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, satellite_id=None, *args, **kwargs):
        super(DataSelectForm, self).__init__(*args, **kwargs)

        if satellite_id is not None:
            result_types = ResultType.objects.filter(
                satellite_id=satellite_id)
            result_list = [(result.result_id, result.result_type)
                                for result in result_types]
            self.fields["result_type"] = forms.ChoiceField(help_text='Select background color of the image that you would like displayed.',
                                                           label='Background Color:', choices=result_list, widget=forms.Select(attrs={'class': 'field-long tooltipped'}))


class GeospatialForm(forms.Form):
    """
    Django form for taking geospatial information for Query requests:
        latitude_min
        latitude_min
        longitude_min
        longitude_max
        time_start
        time_end
    """

    latitude_min = forms.FloatField(label='Min Latitude', widget=forms.NumberInput(
        attrs={'class': 'field-divided', 'step': "any", 'required': 'required'}))
    latitude_max = forms.FloatField(label='Max Latitude', widget=forms.NumberInput(
        attrs={'class': 'field-divided', 'step': "any", 'required': 'required'}))
    longitude_min = forms.FloatField(label='Min Longitude', widget=forms.NumberInput(
        attrs={'class': 'field-divided', 'step': "any", 'required': 'required'}))
    longitude_max = forms.FloatField(label='Max Longitude', widget=forms.NumberInput(
        attrs={'class': 'field-divided', 'step': "any", 'required': 'required'}))
    time_start = forms.DateField(label='Start Date', widget=forms.DateInput(
        attrs={'class': 'datepicker field-divided', 'placeholder': '01/01/2010', 'required': 'required'}))
    time_end = forms.DateField(label='End Date', widget=forms.DateInput(
        attrs={'class': 'datepicker field-divided', 'placeholder': '01/02/2010', 'required': 'required'}))

    def __init__(self, area=None, *args, **kwargs):
        super(GeospatialForm, self).__init__(*args, **kwargs)
        if area is not None:
            self.fields['time_start'] = forms.DateField(initial=area.date_min.strftime("%m/%d/%Y"), label='Start Date', widget=forms.DateInput(attrs={'class': 'datepicker field-divided', 'required': 'required'}))
            self.fields['time_end'] = forms.DateField(initial=area.date_max.strftime("%m/%d/%Y"), label='End Date', widget=forms.DateInput(attrs={'class': 'datepicker field-divided', 'required': 'required'}))
