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
from .functions import (
    get_objs_from_col,
    get_obj_rails,
    reset_export_collection
)


class OBJECT_OT_prepare_export_collection(bpy.types.Operator):
    """Prepare all objects in the active collection for export"""
    bl_idname = "object.prepare_export_collection"
    bl_label = "Prepare Collection for Export"
    bl_options = {'REGISTER', 'UNDO'}
    
    COL_EXPORT = "export"
    GRP_RAILS = "rails"
    
    def execute(self, context):

        col = context.collection
        col_export = reset_export_collection(self.COL_EXPORT)
        print(col.name)
        
        bpy.ops.object.select_all(action='DESELECT')

        if not col:
            self.report({'WARNING'}, "No active collection selected")
            return {'CANCELLED'}
        
        if col.name == "export":
            self.report({'WARNING'}, "Export collection selected")
            return {'CANCELLED'}
        
        objs = get_objs_from_col(col)
        
        if not objs:
            self.report({'WARNING'}, "No objects found in collection")
            return {'CANCELLED'}
        
        for obj in objs:
            print(obj.name)
            get_obj_rails(obj, self.GRP_RAILS, col_export)
        
        return {'FINISHED'}


class OBJECT_OT_debug_meshes(bpy.types.Operator):
    """Clean up mesh data for export"""
    bl_idname = "object.debug_meshes"
    bl_label = "Debug Meshes"
    bl_options = {'REGISTER', 'UNDO'}
        
    def execute(self, context):
        col = context.collection
                
        if not col:
            self.report({'WARNING'}, "No active collection selected")
            return {'CANCELLED'}
        
        objs = get_objs_from_col(col)
        
        if not objs:
            self.report({'WARNING'}, "No objects found in collection")
            return {'CANCELLED'}
        
        for obj in objs:
            print(obj.name)
            get_obj_rails(obj, "rails", None)
        
        bpy.ops.object.select_all(action='DESELECT')
        return {'FINISHED'}


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
