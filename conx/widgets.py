# conx - a neural network library
#
# Copyright (c) Douglas S. Blank <doug.blank@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301  USA

import PIL
import base64
import io

from IPython.display import Javascript, display
from ipywidgets import Widget, register, widget_serialization, DOMWidget
from traitlets import Bool, Dict, Int, Float, Unicode, List, Instance
import matplotlib.pyplot as plt

@register("Camera")
class Camera(DOMWidget):
    """Represents a camera source."""

    # Specify audio constraint and video constraint as a boolean or dict.
    audio = Bool(False).tag(sync=True)
    video = Bool(True).tag(sync=True)

    _view_module = Unicode('camera').tag(sync=True)
    _view_name = Unicode('CameraView').tag(sync=True)
    _model_module = Unicode('camera').tag(sync=True)
    _model_name = Unicode('CameraModel').tag(sync=True)
    image = Unicode('').tag(sync=True)

def get_camera_javascript(width=320, height=240):
    camera_javascript = """
require.undef('camera');

define('camera', ["jupyter-js-widgets"], function(widgets) {
    var CameraView = widgets.DOMWidgetView.extend({
        defaults: _.extend({}, widgets.DOMWidgetView.prototype.defaults, {
            _view_name: 'CameraView',
            _view_module: 'camera',
            audio: false,
            video: true,
        }),

        initialize: function() {

            var div = document.createElement('div');
            var el = document.createElement('video');
            el.setAttribute('id', "video_widget");
            el.setAttribute('width', %(width)s);
            el.setAttribute('height', %(height)s);
            div.appendChild(el);
            var canvas = document.createElement('canvas');
            canvas.setAttribute('id', "video_canvas");
            canvas.setAttribute('width', %(width)s);
            canvas.setAttribute('height', %(height)s);
            div.appendChild(canvas);
            div.appendChild(document.createElement('br'));
            var button = document.createElement('button');
            button.innerHTML = "Take a Picture";
            var that = this;
            button.onclick = function(b) {
                var video = document.querySelector("#video_widget");
                var canvas = document.querySelector("#video_canvas");
                if (video) {
                    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
                    var url = canvas.toDataURL('image/png');
                    if (that.model) {
                        that.model.set('image', url);
                        that.model.save_changes();
                    }
                }
            };
            div.appendChild(button);
            this.setElement(div);
            CameraView.__super__.initialize.apply(this, arguments);
        },

        render: function() {
            var that = this;
             that.model.stream.then(function(stream) {
                 that.el.children[0].src = window.URL.createObjectURL(stream);
                 that.el.children[0].play();
             });
        }
    });

    var CameraModel = widgets.DOMWidgetModel.extend({
        defaults: _.extend({}, widgets.DOMWidgetModel.prototype.defaults, {
            _model_name: 'CameraModel',
            _model_module: 'camera',
            audio: false,
            video: true
        }),

        initialize: function() {
            CameraModel.__super__.initialize.apply(this, arguments);
            // Get the camera permissions
            this.stream = navigator.mediaDevices.getUserMedia({audio: false, video: true});
        }
    });
    return {
        CameraModel: CameraModel,
        CameraView: CameraView
    }
});
""" % {"width": width, "height": height}
    return camera_javascript

@register("Camera")
class Camera(DOMWidget):
    """Represents a media source."""
    _view_module = Unicode('camera').tag(sync=True)
    _view_name = Unicode('CameraView').tag(sync=True)
    _model_module = Unicode('camera').tag(sync=True)
    _model_name = Unicode('CameraModel').tag(sync=True)
    # Specify audio constraint and video constraint as a boolean or dict.
    audio = Bool(False).tag(sync=True)
    video = Bool(True).tag(sync=True)
    image = Unicode("").tag(sync=True)
    image_count = Int(0).tag(sync=True)

    def __init__(self, *args, **kwargs):
        display(Javascript(get_camera_javascript()))
        super().__init__(*args, **kwargs)

    def get_picture(self):
        if self.image:
            return uri_to_image(self.image)

def uri_to_image(image_str, width=320, height=240):
    header, image_b64 = image_str.split(",")
    image_binary = base64.b64decode(image_b64)
    image = PIL.Image.open(io.BytesIO(image_binary)).resize((width, height))
    return image

def plot(lines, width=8.0, height=4.0, xlabel="time", ylabel=""):
    """
    SVG(plot([["Error", "+", [1, 2, 4, 6, 1, 2, 3]]],
             ylabel="error",
             xlabel="hello"))
    """
    plt.rcParams['figure.figsize'] = (width, height)
    fig = plt.figure()
    for (label, symbol, data) in lines:
        kwargs = {}
        args = [data]
        if label:
            kwargs["label"] = label
        if symbol:
            args.append(symbol)
        plt.plot(*args, **kwargs)
    if any([line[0] for line in lines]):
        plt.legend()
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    bytes = io.BytesIO()
    plt.savefig(bytes, format='svg')
    svg = bytes.getvalue()
    plt.close(fig)
    return svg.decode()
