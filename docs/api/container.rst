
Containers
==========


Generic
-------

.. currentmodule:: bv.container

.. automodule:: bv.container

.. autoclass:: Container

    .. attribute:: options
    .. attribute:: container_options
    .. attribute:: stream_options
    .. attribute:: metadata_encoding
    .. attribute:: metadata_errors
    .. attribute:: open_timeout
    .. attribute:: read_timeout


Flags
~~~~~

.. attribute:: bv.container.Container.flags

.. class:: bv.container.Flags

    Wraps :ffmpeg:`AVFormatContext.flags`.

    .. enumtable:: bv.container.core:Flags
        :class: bv.container.core:Container


Input Containers
----------------

.. autoclass:: InputContainer
    :members:


Output Containers
-----------------

.. autoclass:: OutputContainer
    :members:


Formats
-------

.. currentmodule:: bv.format

.. automodule:: bv.format

.. autoclass:: ContainerFormat

.. autoattribute:: ContainerFormat.name
.. autoattribute:: ContainerFormat.long_name

.. autoattribute:: ContainerFormat.options
.. autoattribute:: ContainerFormat.input
.. autoattribute:: ContainerFormat.output
.. autoattribute:: ContainerFormat.is_input
.. autoattribute:: ContainerFormat.is_output
.. autoattribute:: ContainerFormat.extensions

Flags
~~~~~

.. autoattribute:: ContainerFormat.flags

.. autoclass:: bv.format.Flags

    .. enumtable:: bv.format.Flags
        :class: bv.format.ContainerFormat

