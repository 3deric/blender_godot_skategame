import bpy
from ..functions import *


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