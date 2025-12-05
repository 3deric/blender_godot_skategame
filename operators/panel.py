import bpy
from ..operators import *

class VIEW3D_PT_godot_skate_tools(bpy.types.Panel):
    """Panel for export preparation tools"""
    bl_label = "Export Preparation"
    bl_idname = "VIEW3D_PT_export_preparation_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tools"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator("object.prepare_export_collection",
                     text="Setup Export",
                     icon='COLLECTION_NEW')
                    
        row = layout.row()
        row.operator("object.debug_meshes",
                     text="Debug Meshes",
                     icon='MESH_DATA')