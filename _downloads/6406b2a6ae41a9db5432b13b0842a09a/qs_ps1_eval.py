from gradefast.submission import Submission, LoadSubmissions
from gradefast.test import TestType, GFTest
from gradefast.evaluate import Evaluate
from gradefast.aggregate import Aggregate

fs_location = './examples/quickstart1/qs_ps1'
task_name = 'Task1'
theme_name = 'Quickstart'
submission_group = LoadSubmissions.from_fs(fs_location, task_name, theme_name).get_submissions()
print(submission_group)


class QS1Test(GFTest):
    def __init__(self):
        super().__init__(TestType.FILE, 'text')

    def __call__(self, file_path, submission):
        # GFTest requires this method to be implemented
        # we will write evaluation logic here
        
        # expected output
        # each of the correct words fetch different marks
        expected_words = ['Musical', 'Tenzin', 'Random', 'Calcifer', 'Shirucafe']

        # notice the file_path and submission parameters
        # these parameters are inserted in this test automatically
        # by another gradefast module called Evaluate
        result_dict = {}
        with open(file_path, 'r') as text_file:
            submission_words = text_file.readlines()
            # trim spaces and newlines
            submission_words = list(map(lambda submission_word: submission_word.strip(), submission_words))
            count_correct_words = 0
            for word in expected_words:
                if word in submission_words:
                    # for each of the word that is present add that word
                    # in dictionary and set value to 1 
                    result_dict[word] = 1
                    count_correct_words += 1
            return result_dict, 'You guessed {} words properly'.format(count_correct_words), None

test = QS1Test()

# obtain a single submission '4' file path
submission_4_text_path = submission_group[4].items['text']['path']
# run the test
result_dict, comment, exceptions = test(submission_4_text_path,
submission_group[4])

print(result_dict)
print(comment)
print(exceptions)

evaluate = Evaluate(test)
result_group, exceptions = evaluate(submission_group)
print(result_group)
print(exceptions)

total_group = Aggregate.add(result_group)
print(total_group)

weightages = {'Musical': 10, 'Random': 5, 'Tenzin': 35, 'Calcifer': 50, 
'Shirucafe': 30}
weighted_group = Aggregate.multiply(weightages, result_group)
total_group = Aggregate.add(weighted_group)
print(total_group)
