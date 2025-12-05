import bpy
import bmesh
import mathutils


def get_objs_from_col(col):
    objs = []
    objs.extend([obj for obj in col.objects if obj.type == 'MESH'])
    for child_col in col.children:
        objs.extend(get_objs_from_col(child_col))
    return objs


def vertex_overlap(vert1, vert2, threshold=0.001):
    distance = (vert1.co - vert2.co).length
    return distance < threshold


def get_closed(obj):
    if obj and obj.type == 'MESH':
        mesh = obj.data
        vertices = mesh.vertices

        if len(vertices) >= 2:
            first_vert = vertices[0]
            last_vert = vertices[-1]

            return vertex_overlap(first_vert, last_vert)
    return False


def get_obj_rails(obj, vertex_group_name, col_export):
    if obj.type != 'MESH':
        raise ValueError("Object must be a mesh")
        
    vertex_group = obj.vertex_groups.get(vertex_group_name)
    if vertex_group is None:
        return
    
    src_name = obj.name
    
    new_obj = obj.copy()
    new_obj.data = obj.data.copy()

    if col_export:
        col_export.objects.link(new_obj)
    
    bpy.context.view_layer.objects.active = new_obj
    
    vgroup = new_obj.vertex_groups.get(vertex_group_name)
    
    verts_to_keep_indices = set()
     
    for vert in new_obj.data.vertices:
        for vg in vert.groups:
            if vg.group == vgroup.index:
                verts_to_keep_indices.add(vert.index)
                break
    
    if verts_to_keep_indices:
        bm = bmesh.new()
        bm.from_mesh(new_obj.data)
        bm.verts.ensure_lookup_table()
        
        verts_to_delete = []
        for i, vert in enumerate(bm.verts):
            if i not in verts_to_keep_indices:
                verts_to_delete.append(vert)
        
        if verts_to_delete:
            bmesh.ops.delete(bm, geom=verts_to_delete, context='VERTS')
            bm.to_mesh(new_obj.data)
        bm.free()

    new_obj.select_set(True)
    bpy.context.view_layer.objects.active = new_obj
    bpy.ops.mesh.separate(type='LOOSE')
    
    selected_objects = bpy.context.selected_objects
    
    for i, obj in enumerate(selected_objects, start=1):
        if get_closed(obj):
            obj.name = f"{src_name}_Rail_{str(i).zfill(2)}_Closed"
        else:
            obj.name = f"{src_name}_Rail_{str(i).zfill(2)}"
    
    bpy.ops.object.select_all(action='DESELECT')
    return


def reset_export_collection(col_name):
    export_collection = bpy.data.collections.get(col_name)

    if export_collection:
        # Delete all objects in the collection
        objects_to_delete = [obj for obj in export_collection.objects]
        for obj_to_delete in objects_to_delete:
            bpy.data.objects.remove(obj_to_delete, do_unlink=True)

        bpy.data.collections.remove(export_collection)

    export_collection = bpy.data.collections.new(col_name)
    bpy.context.scene.collection.children.link(export_collection)
    return export_collection
