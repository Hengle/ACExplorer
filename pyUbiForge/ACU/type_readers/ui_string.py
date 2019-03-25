from pyUbiForge.misc.file_object import FileObjectDataWrapper
from pyUbiForge.misc.file_readers import BaseReader


class Reader(BaseReader):
	file_type = '81A7045D'

	def __init__(self, py_ubi_forge, file_object_data_wrapper: FileObjectDataWrapper, out_file, indent_count):
		file_object_data_wrapper.read_str(9, out_file, indent_count)
		file_object_data_wrapper.read_id(out_file, indent_count)
		file_object_data_wrapper.read_str(17, out_file, indent_count)
		for _ in range(18):
			py_ubi_forge.read_file.get_data_recursive(file_object_data_wrapper, out_file, indent_count)