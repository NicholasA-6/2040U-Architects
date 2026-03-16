# # You need PyTest for this
# import random
# import back_end
#
#
# class TestBackendClass:
#     @staticmethod
#     def setup_module():
#         data = ""
#         with open("MOCK_DATA.csv", "r+") as file:
#             data = file.read()
#         with open("TEST_DATA.csv", "w+") as file:
#             file.write(data)
#
#     def test_get_user(self):
#         vals = random_strings(3)
#         with open("TEST_DATA.csv", "a") as file:
#             file.write(f"{vals[0]},{vals[1]},{vals[2]}")
#         assert back_end.get_user(vals[0], "TEST_DATA.csv")[0] == [vals[0], vals[1], vals[2]]
#
#     def test_add_to_file(self):
#         vals = random_strings(3)
#         back_end.add_to_file(vals[0], vals[1], vals[2], "TEST_DATA.csv")
#         last_line = ""
#         with open("TEST_DATA.csv", "r") as file:
#             for line in file:
#                 last_line = line.strip()
#         assert last_line == f"{vals[0]},{vals[1]},{vals[2]}"
#
#     def test_replace_user(self):
#         vals = random_strings(5)
#         with open("TEST_DATA.csv", "a") as file:
#             file.write(f"{vals[0]},{vals[1]},{vals[2]}")
#         back_end.replace_user([vals[0], vals[1], vals[2]], [vals[0], vals[3], vals[4]], "TEST_DATA.csv")
#         last_line = ""
#         with open("TEST_DATA.csv", "r") as file:
#             for line in file:
#                 last_line = line.strip()
#         assert last_line == f"{vals[0]},{vals[3]},{vals[4]}"
#
#
#
#
# def random_strings(amount):
#     val = []
#     for i in range(0, 10):
#         val.append(str(random.randint(0, 9999)))
#     return val
#
