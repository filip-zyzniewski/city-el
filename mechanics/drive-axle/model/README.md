# City-EL drive axle CAD model

This model is created using [CadQuery](https://cadquery.readthedocs.io).

## Model files

## Axle model

This model fits both Thrige Titan TTL 140B and Perm PMG132 motor keyways

- [live preview](https://3dviewer.net/#model={{ page.dir | append: 'axle.step' | absolute_url }})
- [GLB format](axle.glb)
- [STEP format](axle.step)
- [STL format](axle.stl)

## Spline cutter model

This is a model of a tool that can be used to cut out
the grooves for the fixed wheel spline.

- [live preview](https://3dviewer.net/#model={{ page.dir | append: 'spline_cutter.glb' | absolute_url }})
- [GLB format](spline_cutter.glb)
- [STEP format](spline_cutter.step)
- [STL format](spline_cutter.stl)

## Working with the model code

The project package is managed using
[uv](https://docs.astral.sh/uv/).

You can install it by following the
[instructions](https://docs.astral.sh/uv/getting-started/installation/).

## Working with CQ-editor

You can use [CQ-editor](https://github.com/CadQuery/CQ-editor) to load
the model and verify the effect of changes made in its code.

### Usage

You can run the editor like this:

```console
~/git/github.com/filip-zyzniewski/city-el/mechanics/drive-axle/model$ uv run edit
```

CQ-editor will run the [script](src/cityel_drive_axle_model/_edit.py)
and display the objects after pressing the [▶] button.

If you want to see the effect of changes in the model code on the result, you
should press the [▶] button again to re-run the script.

#### Troubleshooting

if CQ-editor gives you the following error:

```
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
```

then you can troubleshoot it by setting the `QT_DEBUG_PLUGINS` environment variable to `1`, for example:

```console
~/git/github.com/filip-zyzniewski/city-el/mechanics/drive-axle/model$ QT_DEBUG_PLUGINS=1 uv run edit
[...]
Cannot load library /home/filip/git/github.com/filip-zyzniewski/city-el/mechanics/drive-axle/model/.venv/lib/python3.13/site-packages/PyQt5/Qt5/plugins/platforms/libqxcb.so: (libxcb-xinerama.so.0: cannot open shared object file: No such file or directory)
[...]
~/git/github.com/filip-zyzniewski/city-el/mechanics/drive-axle/model$
```

In this case it's enough to install libxcb-xinerama on your system, for example on ubuntu:

```console
~$ sudo apt install libxcb-xinerama0
[...]
The following NEW packages will be installed:
  libxcb-xinerama0
0 upgraded, 1 newly installed, 0 to remove and 1 not upgraded.
[...]
Unpacking libxcb-xinerama0:amd64 (1.15-1ubuntu2) ...
[...]
~$
```
