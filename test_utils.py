


from utils import *

def test_scope():
	assert(validate_scope("http://test.com/", ["test.com"]))
	assert(not validate_scope("http://test.com/", ["west.com"]))
	assert(validate_scope("http://test.com/", ["west.com", "test.com"]))

def test_merkel():
	tree = merkel_tree(["1", "2", "3"])
	assert(tree.get_hash() == "01e717e7fc0ab59378f7fbffd8eabf0e15151e3d8f995382085aac489786b23f")


def test_parameter():
	key, value = parse_parameters("http:://test.com/wow?test=true")
	assert(key == ["test"])
	assert(value == ["true"])

	key, value = parse_parameters("http:://test.com/wow?test=true&test2=False")
	assert(key == ["test", "test2"])
	assert(value == ["true", "False"])
	
	key, value = parse_parameters("http:://test.com/wow?test=true&test2=False&yes")
	assert(key == ["test", "test2", "yes"])
	assert(value == ["true", "False"])
	
	key, value = parse_parameters("http:://test.com/wow?test=true&test2=&yes=")
	assert(key == ["test", "test2", "yes"])
	assert(value == ["true", "", ""])
	