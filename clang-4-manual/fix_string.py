string_file = "/usr/include/c++/v1/string"
line_num = 1938
insert = ""
insert += "#if _LIBCPP_STD_VER <= 14\n"
insert += "   _NOEXCEPT_(is_nothrow_copy_constructible<allocator_type>::value)\n"
insert += "#else\n"
insert += "    _NOEXCEPT\n"
insert += "#endif\n"


lines = []
with open(string_file, "r") as rf:
    lines = rf.readlines()

out = ''
for line in lines[:line_num]:
    out += line

out += insert

for line in lines[line_num:]:
    out += line

with open(string_file, 'w') as wf:
    wf.write(out)

