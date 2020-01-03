from gradefast.submission import Submission, LoadSubmissions
from gradefast.test import TestType, GFTest
from gradefast.evaluate import Evaluate
from gradefast.aggregate import Aggregate

fs_location = './examples/quickstart2/qs_ps2'
task_name = 'Task2'
theme_name = 'Quickstart'
submission_group = LoadSubmissions.from_fs(fs_location, task_name, theme_name).get_submissions()
print(submission_group)


class QS2Test(GFTest):
    def __init__(self):
        # file_to_test is unzipped which is the name of file_item in
        # e.g. submission.items['unzipped']['path'] resolves path to
        # the unzipped folder on filesystem 
        # package_path is the parent directory where the module or
        # package can be found
        # in this case final path of package is 'unzipped' + './' 
        super().__init__(TestType.PYTHON, 'unzipped', package_path='./')

    def __call__(self, submission):
        # GFTest requires this method to be implemented
        # we will write evaluation logic here
        
        # expected output
        init_list = [[4, 3, 2, 8, 7], [10, 45, 21, 8, 33], [8, 52, 16, 77, 2]]
        sorted_list = [[2, 3, 4, 7, 8], [8, 10, 21, 33, 45], [2, 8, 16, 52, 77]]

        # notice the file_path and submission parameters
        # these parameters are inserted in this test automatically
        # by another gradefast module called Evaluate
        result_dict = {}
        result_dict['marks'] = []
        try:
            import sortalg
        except Exception as e:
            return result_dict, '', e.message
        
        for i in range(3):
            output = sortalg.quicksort(init_list[i])
            if output == sorted_list[i]:
                result_dict['marks'].append(1)
            else:
                result_dict['marks'].append(0)
        return result_dict, '', None

test = QS2Test()

# obtain a single submission '4' file path
# submission_4_text_path = submission_group[4].items['unzipped']['path']
# run the test
# result_dict, comment, exceptions = test(submission_group[4]) # throws module
# not found error

# when importing modules better use Evaluate
evaluate = Evaluate(test)
result_group, exceptions = evaluate(submission_group)
print(result_group)
print(exceptions)

# weightages
weightages = {}
weightages['marks'] = [5, 10, 15]
# scaling
scaled_result_group = Aggregate.multiply(weightages, result_group)
# calculating total
total_group = Aggregate.add(scaled_result_group, average=False)
print(total_group)

# adding comments based on marks
def build_comment(result):
    if result.result_dict['total'] == 30:
        return 'well done'
    return 'no worries. try and complete the task'

total_group.comment_builder(build_comment)
total_and_comments = total_group.make_comments()
print(total_and_comments)
