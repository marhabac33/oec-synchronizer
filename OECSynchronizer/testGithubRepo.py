from oec_sync_utils.github_repo import GitRepo
import unittest, os

class TestGithubRepo(unittest.TestCase):

    def setUp(self):
        # Test if the setup class was ran?
        (self.oauth, self.oauth_id, self.origin_user, self.origin_repo,\
        self.up_user, self.up_repo) = ('427f36bb6faafacbdd61934e5754296fd0c885bd',\
        '', 'ziaahsan', 'oec_test_master', 'Mr-Ian-Ferguson', 'oec_test_master')

        self.gitRepo = GitRepo(self.oauth, self.oauth_id,\
        self.origin_user, self.origin_repo, self.up_user, self.up_repo)

    def test_github_init(self):
        #Testing github init
        self.assertEqual(None, self.gitRepo.path(),\
        self.origin_repo + " was not cloned correctly.")

    def test_github_clone(self):
        # Testing github clone
        self.assertFalse(self.gitRepo.clone(), self.origin_repo +\
        " failed to clone.")


    def test_github_exists(self):
        #Testing the existance of the repo
        self.assertFalse(self.gitRepo.exists(), "Repo: "+self.origin_repo +\
        " Does not exist.")



if __name__ == '__main__':
    unittest.main()
