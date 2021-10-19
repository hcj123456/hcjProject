from testcases.models import Testcases


def get_testcases_by_interface_ids(ids_list):
    one_list = []
    for interface_id in ids_list:
        testcases_qs = Testcases.objects.values_list('id', flat=True).filter(interface_id=interface_id)
        one_list.extend(list(testcases_qs))
    return one_list