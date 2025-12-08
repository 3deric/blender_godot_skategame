import bpy
from ..functions import *


class OBJECT_OT_prepare_export_collection(bpy.types.Operator):
    """Prepare all objects in the active collection for export"""
    bl_idname = "object.prepare_export_collection"
    bl_label = "Prepare Collection for Export"
    bl_options = {'REGISTER', 'UNDO'}
    
    COL_EXPORT = "export"
    GRP_RAILS = "rails"
    GRP_FLOOR = "floor"
    GRP_WALL = "wall"
    GRP_PIPE = "pipe"
    GRP_MESH = "mesh"

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
            get_obj_colliders(obj, self.GRP_FLOOR, col_export)
            get_obj_colliders(obj, self.GRP_WALL, col_export)
            get_obj_colliders(obj, self.GRP_PIPE, col_export)
            get_obj_mesh(obj, self.GRP_MESH, col_export)
        
        return {'FINISHED'}