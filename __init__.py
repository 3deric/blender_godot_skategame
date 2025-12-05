bl_info = {
    "name": "Godot Skate Tools",
    "author": "Eric Schubert",
    "version": (1, 0),
    "blender": (4, 5, 3),
    "location": "3D View > Sidebar > Godot Skate",
    "description": "Toolset for my Godot Skateboarding Game",
    "category": "Object",
}

import bpy

from .operators import OBJECT_OT_debug_meshes
from .operators import OBJECT_OT_prepare_export_collection
from .operators import VIEW3D_PT_godot_skate_tools

classes = [
    OBJECT_OT_prepare_export_collection,
    OBJECT_OT_debug_meshes,
    VIEW3D_PT_godot_skate_tools,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
