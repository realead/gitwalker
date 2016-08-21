import unittest

import sys
sys.path.append('../src')

import gwlib.processcall as pc

class ProcessCallTester(unittest.TestCase):
        
    def test_run_success(self):
        call_result=pc.execute_process(["sh", "scripts/process_call_test.sh"], ok_code=[0,42])
        self.assertEqual(call_result.returncode, 42)
        self.assertEqual(call_result.stdout, "stdout\n")
        self.assertEqual(call_result.stderr, "stderr\n")
      
        
    def test_run_not_expected_result(self):
        with self.assertRaises(pc.ProcessCallError) as context:
            pc.execute_process(["sh", "scripts/process_call_test.sh"])
        self.assertTrue('Process returned unexpected code 42' in context.exception)
        self.assertEqual(context.exception.returncode, 42)
        
