"""
run "python manage.py test transaction>test_results/transaction_testresult.txt"

Author: Mark Scrimshire @ekivemark

"""

__author__ = 'mark @ekivemark'

from django.test import TestCase
from ..accounts.models import User, UserProfile
from ..tests.test_utils import *
from ..tests.settings_test import *

import inspect
import uuid

"""
Tests for the flangio.transaction app.

Run from root of flangio app.
Run with "python manage.py test {app name}"
Example: python manage.py test transaction >./test_results/transaction_testresult.txt

Remember: every test definition must begin with "test_"

Generate the test data properly indented for readability
python manage.py dumpdata transaction --indent=4 >./apps/transaction/fixtures/testdata.json

"""

# Add module specific test variables here

# End of Module specific test variables section


# SimpleTest for a working Test Harness
# @unittest.skip
class Transaction_Simple_TestCase(TestCase):
    """Background to this test harness
       and prove the test harness works
    """

    # Add your fixtures here
    fixtures = [#'testdata.json',
                '../accounts/fixtures/testdata.json']

    def test_basic_addition_Transaction(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        Test_Start("1+1=2")
        answer = self.assertEqual(1 + 1, 2)
        Test_Msg("flangio.apps.transaction.tests.py")
        print "     Test Runtime: "+str(datetime.now())
        if answer == None:
            print "     Test Harness ready"
        else:
            print "     This Test Harness has a problem"
        Test_End("flangio.apps.transaction.tests.py")

        return

    def test_load_home_page(self):
        """
        Test that we are loading the home page
        """

        Test_Start()

        showprint = False

        Test_Msg("Go to Home Page for flangio")

        # Transaction create should test for an existing account
        usrname = ""
        passwd  = ""
        # reset output
        output = []
        post_url = "/"
        post_parameters = {}
        called_by  = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        looked_for = HOME_PAGE_TITLE_TEXT

        # set page code expected to be returned
        code_return = 200
        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for, False)


        Test_End()

class Transaction_Create_TestCase(TestCase):
    """
    Create transactions and store in flangio

    /transaction/create

    #get all features that match the search dict (returns a json list of feature_ids)
    /transaction/search.json
    /transaction/search.csv
    /transaction/search.xls

    #get a transaction by txid (returns a json object)
    /transaction/<txid>.json

    /transaction/since/<sinceid>.json


    Test Plan:
    1. Create a series of Transactions
    2. Save the Transaction Ids
    3. Search for specific Transactions
    4. Get a specific Transaction by Id
    5. Get a group of Transactions using an earlier transaction as a starting point

    """

    # Add your fixtures here
    # fixtures = ['testdata.json']

    def test_failed_create_transaction(self):
        """
        Fail at Create transaction in flangio

        """
        Test_Start()

        showprint = True

        # We need to create a user account
        user_info = create_user_account(self, USERNAME_FOR_TEST, EMAIL_FOR_TEST, PASSWORD_FOR_TEST, showprint)

        check_permission(USERNAME_FOR_TEST,True)

        Test_Msg("Transaction - Force a failure")

        # No need to be logged in to get the home page.
        usrname = USERNAME_FOR_TEST
        passwd  = PASSWORD_FOR_TEST
        # reset output
        output = []
        post_url = "/transaction/create"
        post_parameters = {
                           "transaction_type":"text",
                           "text":"Some Text",
                           }
        called_by  = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        looked_for = "No transaction was created. The transaction failed due to the following error(s)."

        code_return = 500
        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for, False)


        showprint = False

        usrname = USERNAME_FOR_TEST
        passwd  = PASSWORD_FOR_TEST
        # reset output
        output = []
        post_url = "/transaction/create"
        post_parameters = {
                           "transaction_type":"text",
                           "text":"Some Text",
                           "subject": USERNAME_FOR_TEST,
                           "receiver": USERNAME_FOR_TEST,
                           "sender": USERNAME_FOR_TEST,
                           "security_level": "2",
                           "transaction_timezone": "0",
                           "transaction_datetime": "2012-04-17 16:50:55",
                           "event_datetime": "2012-04-17 12:50:55",
                           "event_timezone": "0",
                           "event_date": "2012-04-17",
                           "transaction_id": str(uuid.uuid4()),
                           }
        called_by  = inspect.getframeinfo(inspect.currentframe().f_back)[2]

        looked_for = "Transaction created."

        code_return = 200
        result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint )

        if showprint != False:
            print "Result:" + str(result)
            print output

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for)
        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for, False)



        Test_End()

        return

    def test_create_transactions(self):
        """
        Now test a series of transactions being created.
        """

        Test_Start()

        showprint = False

        # We need to create a user account
        usrname = USERNAME_FOR_TEST
        passwd  = PASSWORD_FOR_TEST

        user_info = create_user_account(self, USERNAME_FOR_TEST, EMAIL_FOR_TEST, PASSWORD_FOR_TEST, showprint)

        check_permission(USERNAME_FOR_TEST, True)
        give_permission(USERNAME_FOR_TEST,"assign-points")


        post_url = "/transaction/create"
        called_by  = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        output = []
        looked_for = "Transaction created."

        transaction_history = {}

        showprint = True
        code_return = 200
        for i in range(1,20,1):
            output = []
            transaction_history[str(i)] = str(uuid.uuid4())
            print transaction_history[str(i)]
            post_parameters = {
                "transaction_type":"text",
                "text":"Some Text-"+str(i),
                "subject": USERNAME_FOR_TEST,
                "receiver": USERNAME_FOR_TEST,
                "sender": USERNAME_FOR_TEST,
                "security_level": "2",
                "transaction_timezone": "0",
                "transaction_datetime": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                "event_datetime": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                "event_timezone": "0",
                "points":str(i),
                "event_date": str(datetime.now().strftime("%Y-%m-%d")),
                "transaction_id": transaction_history[str(i)],
                }

            result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint )
            if showprint != False:
                print "Result:" + str(result)
                print output

            if result == None:
                Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for+ " - "+str(i))

            else:
                Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for+ " - "+str(i),False)

        print transaction_history

        print transaction_history["5"]
        Test_End()

        Test_Start("Now we can look for some Transactions...")

        post_url = "/transaction/since"+transaction_history["5"]+".json"

        output = []
        code_return = 200

        post_parameters = {}
        looked_for = transaction_history["5"]

        # result = test_for_post(self, code_return, usrname, passwd, output, post_url,post_parameters, looked_for, called_by, showprint )
        if showprint != False:
            print "Result:" + str(result)
            print output

        if result == None:
            Test_Msg("Successful Test for "+str(code_return)+ " - " + looked_for+ " - "+str(i))

        else:
            Test_Msg("Test Failed for "+str(code_return) + " - " + looked_for+ " - "+str(i),False)


        Test_End()


        return