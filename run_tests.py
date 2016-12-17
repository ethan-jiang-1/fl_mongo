#!/usr/bin/env python
# encoding:utf8

import os
import subprocess
import glob
import sys
import string
import signal
import random
from xml.dom.minidom import parse
from datetime import datetime


_tool_version = "0.1.0"


def signal_exit_handler(signal, frame):
    print('Stop Running as SIGINT/SIGTERM received')
    sys.exit(0)


class Runner():

    def __init__(self, test_flags, nosetests_flags):
        # stop the runner
        signal.signal(signal.SIGINT, signal_exit_handler)
        signal.signal(signal.SIGTERM, signal_exit_handler)

        self.root_folder = os.getcwd()
        self.test_flags = test_flags
        self.nosetests_flags = nosetests_flags

        self.log_main_filename = self.root_folder + "/log/run_tests_main.log"
        self.log_sum_filename = self.root_folder + "/log/run_tests_sum.log"

        self.result_all = {}
        self.result_all_seconds = 0
        self.result_all_cases = 0
        self.result_all_passed = 0
        self.result_all_failed = 0
        self.result_all_error = 0
        self.result_all_failed_case_names = []
        self.result_all_error_case_names = []

        xml_path = self.root_folder + "/log/rt_xml"
        if not os.path.isdir(xml_path):
            os.makedirs(xml_path)

        self.skip_folders = []
        self.skip_tags = {}
        self.prepare_skip_flags()

    def run_all(self):
        self.prompt_start("Runner run_all under tests")
        subfolders = glob.glob('./tests/test*')

        for subfolder in subfolders:
            sub_working_dir = self.root_folder + "/" + subfolder[2:]
            if not self.skip_folder(subfolder):
                self.run_command_nosetests(sub_working_dir, True)
            else:
                self.log_main_stdout("## Skip test(s) under: " + subfolder)

        self.summarize_result()

    def run_folder(self, sub_working_dir):
        self.prompt_start("Runner run_folder " + sub_working_dir)

        self.run_command_nosetests(sub_working_dir, True)

        self.summarize_result()

    def run_one(self, file_name):
        self.prompt_start("Runner run_one " + file_name)

        self.run_command_nosetests(file_name, False)

        self.summarize_result()

    def prepare_skip_flags(self):
        for skip in self.test_flags:
            if skip.startswith("skip_folder"):
                s = skip.split("=")
                if len(s) > 1:
                    names = s[1].split(":")
                    self.skip_folders = names
            elif skip.startswith("skip_tag_"):
                s = skip.split("=")
                if len(s) > 1:
                    tags = s[0].split("skip_tag_")
                    self.skip_tags[tags[1]] = s[1]

    def skip_folder(self, folder):
        for skip_folder in self.skip_folders:
            if folder.find(skip_folder) != -1:
                return True
        return False

    def prompt_start(self, msgs):
        self.log_main_sum_stdout("")
        self.log_main_sum_stdout("Start Test - session-" + str(random.randint(1000, 9999)))
        self.log_main_sum_stdout(msgs)
        # self.log_main_sum_stdout( "Runner test_flags: " +  str(self.test_flags))
        if len(self.skip_folders) > 0:
            self.log_main_stdout("Skip folders (substring contains): " + str(self.skip_folders))
        if len(self.skip_tags) > 0:
            self.log_main_stdout("Skip tags: " + str(self.skip_tags))
        if len(self.nosetests_flags) > 0:
            self.log_main_stdout("Nosetest flags: " + str(self.nosetests_flags))

    def summarize_timespan(self):
        cases = []
        for suite in self.result_all:
            result_suite = self.result_all[suite]
            if "cases" in result_suite:
                rs = result_suite["cases"]
                for r in rs:
                    cases.append(r)

        sorted_cases = sorted(cases, cmp=lambda x, y: cmp(y["time"], x["time"]))
        self.log_sum("\n")
        self.log_sum("Sorted time span on cases:\n")
        for sc in sorted_cases:
            msg = "\t{0}s\t {1} {2}\n".format(sc["time"], sc["classname"], sc["name"])
            self.log_sum(msg)

    def summarize_result(self):
        self.log_main_sum_stdout("")
        self.log_main_sum_stdout("Total\t{0} test cases found and executed.".format(self.result_all_cases))
        self.log_main_sum_stdout("Result\t{0} passed \t{1} \tfailed {2} error.".format(self.result_all_passed, self.result_all_failed, self.result_all_error))
        self.log_main_sum_stdout("Total timespan in Shell: %.2fs" % self.result_all_seconds)

        if len(self.result_all_failed_case_names) != 0 or len(self.result_all_error_case_names) != 0:
            self.log_main_sum_stdout("List of Failed/Error class: (class name can be rerun by nosetests or runner directly)")
            for failed_case_name in self.result_all_failed_case_names:
                self.log_main_sum_stdout("\tF\t" + self.get_class_name_of_case(failed_case_name))

            for failed_case_name in self.result_all_error_case_names:
                self.log_main_sum_stdout("\tE\t" + self.get_class_name_of_case(failed_case_name))

        self.summarize_timespan()

    def get_class_name_of_case(self, case_name):
        names = string.split(case_name, '.')
        nlen = len(names)
        last_name = names[nlen - 1]
        names.remove(last_name)
        ret = '.'.join(names)
        return ret

    def log_main_sum_stdout(self, msgs):
        print(msgs)
        self.log_main(msgs + "\n")
        self.log_sum(msgs + "\n")

    def log_main_stdout(self, msgs):
        print(msgs)
        self.log_main(msgs + "\n")

    def log_main(self, msgs):
        fh = open(self.log_main_filename, 'a')
        fh.writelines(msgs)
        fh.close()

    def log_sum(self, msgs):
        fh = open(self.log_sum_filename, 'a')
        fh.writelines(msgs)
        fh.close()

    def get_xml_name(self, test_line):
        names = string.split(test_line, '/')
        nlen = len(names)
        if len(names[nlen - 1]) != 0:
            return names[nlen - 1]
        return names[nlen - 2]

    def prepare_nosetest_command(self, test_line, is_subfolder):
        test_name = self.get_xml_name(test_line)
        xml_name = 'log/rt_xml/' + test_name + ".xml"
        xml_pathname = self.root_folder + '/' + xml_name

        command = ['nosetests',
                    test_line,
                    '--with-xunit',
                    '--xunit-file=' + xml_name]

        if len(self.nosetests_flags) > 0:
            for tag in self.nosetests_flags:
                command.append(tag)

        cmd_line = ' '.join(command)

        return command, cmd_line, test_name, xml_pathname

    def run_command_nosetests(self, test_line, is_subfolder):
        start_time = datetime.now()

        command, cmd_line, test_name, xml_pathname = self.prepare_nosetest_command(test_line, is_subfolder)

        self.log_main_stdout("## Auto execute tests: " + cmd_line)

        if os.path.isfile(xml_pathname):
            os.remove(xml_pathname)

        if len(self.nosetests_flags) > 0:
            subprocess.call(command)

        else:
            p = subprocess.Popen(command,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
            lines = p.stdout.readlines()

            self.log_main("\n")
            self.log_main(cmd_line + "\n")
            self.log_main(lines)

        end_time = datetime.now()
        time_span = end_time - start_time
        this_seconds = time_span.total_seconds()
        time_span_str = " - Timespan in Shell: %.2fs" % this_seconds

        if os.path.isfile(xml_pathname):
            result = self.analyse_result(xml_pathname, test_line, is_subfolder, test_name)
            self.log_main_stdout("# Run " + result + time_span_str)
        else:
            self.log_main_stdout("# No Result found")

        self.result_all_seconds += this_seconds

    def make_no_pass_message(self, no_pass_name, case, fe_info):

        fe_log = fe_info["data"]
        fe_type = fe_info["type"]

        msg = "\n========== "
        msg += no_pass_name + ": " + case["classname"] + "\n"

        logs = fe_log.split("\n")
        nlen = len(logs)
        if nlen > 0:
            last_line = logs[nlen - 1]
            logs[nlen - 1] = ""

            msg += 'Traceback:\n'
            msg += '\n'.join(logs)

            msg += fe_type + ": "
            nll = len(last_line)
            if nll > 0 and last_line[0] == '\'' and last_line[nll - 1] == '\'':
                last_line = last_line.replace('\'', '')
                last_line = last_line.replace("\\n", "\n")
                last_line_logs = last_line.split("\n")
                msg += last_line_logs[0]

        return msg

    def fill_no_passed(self, fe_nodes, case, no_pass_name):
        msg = "\n"
        fe_info = {}
        case[no_pass_name] = fe_info

        for fe in fe_nodes:
            fe_info["type"] = fe.getAttribute("type")
            fe_info["message"] = fe.getAttribute("message")

            details = fe.firstChild
            if details is not None:
                fe_info["data"] = details.data
                msg += self.make_no_pass_message(no_pass_name, case, fe_info)
        msg += "\n"

        return msg

    def analyse_result(self, xml_pathname, test_line, is_subfolder, test_name):
        info = {}
        cases = []

        passed_cnt = 0
        failed_cnt = 0
        error_cnt = 0
        dom = parse(xml_pathname)
        if dom is not None:
            for nodeSuite in dom.childNodes:
                info["suite_tests"] = nodeSuite.getAttribute("tests")
                info["suite_errors"] = nodeSuite.getAttribute("errors")
                info["suite_failures"] = nodeSuite.getAttribute("failures")
                info["suite_skip"] = nodeSuite.getAttribute("skip")

                for nodeCase in nodeSuite.childNodes:
                    case = {}
                    case["classname"] = nodeCase.getAttribute("classname")
                    case["name"] = nodeCase.getAttribute("name")
                    case["time"] = float(nodeCase.getAttribute("time"))

                    failures = nodeCase.getElementsByTagName("failure")
                    errors = nodeCase.getElementsByTagName("error")

                    if len(failures) == 0 and len(errors) == 0:
                        passed_cnt += 1
                    else:
                        msg = ""
                        if len(failures) != 0:
                            msg = self.fill_no_passed(failures, case, "Failure")
                            failed_cnt += 1
                            self.result_all_failed_case_names.append(case["classname"])

                        if len(errors) != 0:
                            msg = self.fill_no_passed(errors, case, "Error")
                            error_cnt += 1
                            cname = case["classname"]
                            cname += " >>> " + errors[0].getAttribute("type") + " @ " + errors[0].getAttribute("message") + "."
                            self.result_all_error_case_names.append(cname)

                        if not is_subfolder:
                            print(msg)

                    cases.append(case)

        total_cnt = passed_cnt + failed_cnt + error_cnt
        info["total_cnt"] = total_cnt
        info["passed_cnt"] = passed_cnt
        info["failed_cnt"] = failed_cnt
        info["error_cnt"] = error_cnt
        info["xml"] = xml_pathname
        info["test_name"] = test_name
        info["test_line"] = test_line
        info["is_subfolder"] = is_subfolder

        result = {}
        result["info"] = info
        result["cases"] = cases

        self.result_all[test_name] = result
        self.result_all_cases += total_cnt
        self.result_all_passed += passed_cnt
        self.result_all_failed += failed_cnt
        self.result_all_error += error_cnt

        msg = "\t{0} cases: \t{1} passed \t{2} failed \t{3} error".format(total_cnt, passed_cnt, failed_cnt, error_cnt)
        return msg


def show_help():
    print("Python Unit-Test Runner {0}".format(_tool_version))
    print("  Usage:")
    print("  ./run_tests.py [options]                           Run all tests ")
    print("  ./run_tests.py [options]   path_to_a_sub_folder    Run all tests under a particular folder")
    print("  ./run_tests.py [options]   path_to_a_py_test.py    Run a particular test")
    print("  ./run_tests.py [options]   path_to_a_case_dots     Run a particular test folder.class")
    print("")
    print("  [options]  options for run_tests or nosetests ")
    print("    --skip_ leading options are filter to run_test, such as: ")
    print("         --skip_folder=xxx[:yyy]+    skip tests under folder:  folder name has xxx/yyy as substring")
    print("         --skip_tag_aaa=ooo          skip tests by tag: aaa = ooo")
    print("    -/-- leading options are for nosetests, such as:")
    print("         -s          not capure stdout")
    print("         --pdb       drop into debug on failures or errors   ")
    print("    -h --help")
    print("         this usage")


def is_class_name(name):
    names = string.split(name, '.')
    nlen = len(names)
    if nlen >= 3:
        last_name = names[nlen - 1]
        names.remove(last_name)
        last_name = names[nlen - 2]
        names.remove(last_name)
        folder = os.getcwd() + '/' + '/'.join(names)
        if os.path.isdir(folder):
            return True
    return False


def main_run():
    test_flags = []
    nosetests_flags = []
    test_full_folder_name = None
    test_full_file_name = None

    root_folder = os.getcwd()

    for arg in sys.argv:
        if arg.startswith('--skip_'):
            test_flags.append(arg[2:].strip())
        elif arg.startswith('-'):
            nosetests_flags.append(arg.strip())
            if arg == "-h" or arg == "-help" or arg == "--help":
                return show_help()
        else:
            if arg != __file__:
                full_folder_or_file = arg

                if not arg.startswith('/'):
                    if arg.startswith('./'):
                        full_folder_or_file = root_folder + '/' + arg[2:]
                    else:
                        full_folder_or_file = root_folder + '/' + arg

                if os.path.isdir(full_folder_or_file):
                    test_full_folder_name = full_folder_or_file

                    if not full_folder_or_file.endswith('/'):
                        test_full_folder_name += "/"

                elif os.path.isfile(full_folder_or_file):
                    t_file_name, t_file_extension = os.path.splitext(full_folder_or_file)
                    if len(t_file_extension) != 0 and t_file_extension == '.py':
                        test_full_file_name = full_folder_or_file

                elif is_class_name(arg):
                    test_full_file_name = arg
                else:
                    print("Error: Unknown parameter or file/folder name: " + arg)
                    return show_help()

    if ("help" in test_flags) or ("help" in nosetests_flags):
        return show_help()

    runner = Runner(test_flags, nosetests_flags)
    if test_full_folder_name is not None:
        return runner.run_folder(test_full_folder_name)
    elif test_full_file_name is not None:
        return runner.run_one(test_full_file_name)
    else:
        return runner.run_all()


if __name__ == '__main__':
    main_run()

