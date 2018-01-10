import sys
import unittest

sys.path.append('../')
from app.ParanuaraDB import ParanuaraDB
 
class TestParanuaraDB(unittest.TestCase):
 
    def setUp(self):
        self.db = ParanuaraDB("resources/companies.json", "resources/people.json")

    def test_db_loaded_companies(self):
        result = self.db.getNumberOfCompanies()
        assert(result > 0)
    
    def test_db_loaded_people(self):
        result = self.db.getNumberOfPeople()
        assert(result > 0)
 
    def test_db_created_dic(self):
        result = self.db.getNumberOfMappedPeople()
        assert(result > 0)

    def test_db_returns_true_for_true_companies(self):
        result = self.db.hasCompany("NETBOOK")
        self.assertTrue(result)
        
    def test_db_returns_false_for_false_companies(self):
        result = self.db.hasCompany("NoCompanyName")
        self.assertFalse(result)

    def test_db_case_insensitive_companies(self):
        result = self.db.hasCompany("NeTbOOk")
        self.assertTrue(result)
        
    def test_db_returns_true_for_true_person(self):
        result = self.db.hasPerson("Carmella Lambert")
        self.assertTrue(result)
        
    def test_db_returns_false_for_false_person(self):
        result = self.db.hasPerson("Jack NoName")
        self.assertFalse(result)

    def test_db_get_personal_information_existing_person(self):
        result = self.db.getPersonalInformation("Carmella Lambert")
        assert(len(result) == 22 and result["gender"] == "female")
    
    def test_db_get_personal_information_non_existing_person(self):
        result = self.db.getPersonalInformation("Jack NoName")
        assert(result == dict())
    
    def test_db_finding_employees(self):
        result = self.db.getEmployeesList("NORALI")
        assert(len(result) > 0)
        
    def test_db_finding_employees_in_non_existing_company(self):
        result = self.db.getEmployeesList("NoCompanyName")
        assert(result == list())        
        
    def test_db_get_common_friends_two_existing_people_with_common_friends(self):
        result = self.db.getCommonFriends("Barrett Lambert", "Rosemary Hayes") #"Barrett Lambert")
        assert(result == ["Decker Mckenzie", "Mindy Beasley"])  
    
#   Everybody is friend of Carmella Lambert at least
#    def test_db_get_common_friends_two_existing_people_with_no_common_friends(self):
#        result = self.db.getCommonFriends("Carmella Lambert", "Decker Mckenzie") #"Barrett Lambert")
#        assert(result == list())  
        
    def test_db_get_common_friends_two_non_existing_people(self):
        result = self.db.getCommonFriends("Jack NoName", "Alan Smithee")
        assert(result == list())  

    def test_db_get_common_friends_both_existing_and_non_existing_people(self):
        result = self.db.getCommonFriends("Carmella Lambert", "Alan Smithee")
        assert(result == list())  
        
    def test_db_get_common_friends_two_existing_people_with_no_common_friends(self):
        result = self.db.getCommonFriends("Carmella Lambert", "Ddecker Mckenzie")
        assert(result == list())  
          
    def test_db_parsing_validation(self):
        result = self.db.parseInput("CompanyA")
        assert(result == ["CompanyA"])
        result = self.db.parseInput("CompanyA, CompanyB")
        assert(result == ["CompanyA", "CompanyB"])
        result = self.db.parseInput(" CompanyA     , CompanyB CompanyA,  CompanyB  ")
        assert(result == ["CompanyA", "CompanyB CompanyA", "CompanyB"])
        result = self.db.parseInput(" CompanyA . CompanyB")
        assert(result == ["CompanyA . CompanyB"])
        result = self.db.parseInput(" CompanyA / CompanyB . \;/ CompanyC +.-*/&%$#@ , CompanyD ")
        assert(result == ["CompanyA / CompanyB . \;/ CompanyC +.-*/&%$#@", "CompanyD"])
    
#    Tests for companies
    def test_db_check_input_for_existing_company(self):
        result = self.db.checkInputForCompanies(["NETBOOK"])
        assert(result == [True])
        
    def test_db_check_input_for_non_existing_company(self):
        result = self.db.checkInputForCompanies(["NoCompanyName"])
        assert(result == [False])
        
    def test_db_check_input_for_existing_companies(self):
        result = self.db.checkInputForCompanies(["NETBOOK", "PERMADYNE", "STRALUM"])
        assert(result == [True, True, True])
        
    def test_db_check_input_for_non_existing_companies(self):
        result = self.db.checkInputForCompanies(["NoCompanyName", "NoCompanyName2"])
        assert(result == [False, False])
    
    def test_db_check_input_for_both_existing_and_non_existing_companies(self):
        result = self.db.checkInputForCompanies(["NoCompanyName", "STRALUM"])
        assert(result == [False, True])    
    
#    Tests for people
    def test_db_check_input_for_existing_person(self):
        result = self.db.checkInputForPeople(["Carmella Lambert"])
        assert(result == [True])
        
    def test_db_check_input_for_non_existing_person(self):
        result = self.db.checkInputForPeople(["Jack NoName"])
        assert(result == [False])
        
    def test_db_check_input_for_existing_people(self):
        result = self.db.checkInputForPeople(["Carmella Lambert", "Decker Mckenzie", "Barrett Lambert"])
        assert(result == [True, True, True])
        
    def test_db_check_input_for_non_existing_people(self):
        result = self.db.checkInputForPeople(["Jack NoName", "Alan Smithee"])
        assert(result == [False, False])
    
    def test_db_check_input_for_both_existing_and_non_existing_people(self):
        result = self.db.checkInputForPeople(["Jack NoName", "Carmella Lambert"])
        assert(result == [False, True])
        
#   Tests for final output results
    def test_db_validate_single_company_input(self):
        result = self.db.validateInput("GEOFORM")
        assert(result == "Employees at GEOFORM:\n\tHeidi Hudson\n\tOlivia Leblanc\n\tKelley Holcomb\n\tHolland Sharpe\n\tBrandy James\n")   

    def test_db_validate_multi_company_input(self):
        result = self.db.validateInput("GEOFORM, BEZAL")
        assert(result == "Employees at GEOFORM:\n\tHeidi Hudson\n\tOlivia Leblanc\n\tKelley Holcomb\n\tHolland Sharpe\n\tBrandy James\n" \
               "Employees at BEZAL:\n\tAutumn Greene\n\tStrickland Gonzalez\n\tWillie Horn\n\tJustice Pugh\n")   
    
    def test_db_validate_two_people_input(self):
        result = self.db.validateInput("Carmella Lambert, Barrett Lambert")
        assert(result == "Information about Carmella Lambert:\n\tAge: 61\n\tAddress: 628 Sumner Place, Sperryville, American Samoa, 9819\n\tPhone: +1 (910) 567-3630\n" \
               "Information about Barrett Lambert:\n\tAge: 28\n\tAddress: 618 Sumner Place, Sperryville, Minnesota, 4964\n\tPhone: +1 (810) 488-2604\n"\
               "\nTheir common, alive and brown eyed, friend(s) is/are: Decker Mckenzie")   
        
    def test_db_validate_two_people_input_with_both_existing_and_non_existing_people(self):
        result = self.db.validateInput("Jack NoName, Barrett Lambert, Alan Smithee")
        assert(result == "Warning: \"Jack NoName, Alan Smithee\" was not found in our Data Base! Aborting Search...\nPlease, check for misspelling and try again!")   
    
    def test_db_validate_one_person_input(self):
        result = self.db.validateInput("Barrett Lambert")
        assert(result == "{\"username\": \"barrettlambert@earthmark.com\", \"age\": \"28\", \"fruits\": [\"orange\", \"apple\", \"strawberry\"], \"vegetables\": [\"carrot\"]}")

    def test_db_validate_more_than_two_people_input(self):
        result = self.db.validateInput("Barrett Lambert, Carmella Lambert, Decker Mckenzie")
        assert(result == "No matches...\nPlease, type only company name(s) OR 1 or 2 people names per search")

    def test_db_validate_one_non_existing_person_input(self):
        result = self.db.validateInput("Jack NoName")
        assert(result == "Warning: \"Jack NoName\" was not found in our Data Base! Aborting Search...\nPlease, check for misspelling and try again!")

    def test_db_validate_one_existing_company_one_existing_person_input(self):
        result = self.db.validateInput("NETBOOK, Barrett Lambert")
        assert(result == "No matches...\nPlease, type only company name(s) OR 1 or 2 people names per search")
    
    def test_db_validate_one_existing_person_one_existing_company_input(self):
        result = self.db.validateInput("Barrett Lambert, NETBOOK")
        assert(result == "No matches...\nPlease, type only company name(s) OR 1 or 2 people names per search")

    def test_db_validate_one_non_existing_company_one_existing_person_input(self):
        result = self.db.validateInput("NoCompany, Barrett Lambert")
        assert(result == "Warning: \"NoCompany\" was not found in our Data Base! Aborting Search...\nPlease, check for misspelling and try again!")

    def test_db_validate_one_non_existing_person_one_existing_company_input(self):
        result = self.db.validateInput("Jack NoName, NETBOOK")
        assert(result == "Warning: \"Jack NoName\" was not found in our Data Base! Aborting Search...\nPlease, check for misspelling and try again!")

    def test_db_validate_non_existing_company_and_non_existing_person_input(self):
        result = self.db.validateInput("NoCompany, Jack NoName")
        assert(result == "Warning: \"NoCompany, Jack NoName\" was not found in our Data Base! Aborting Search...\nPlease, check for misspelling and try again!")
    
if __name__ == '__main__':
    unittest.main()