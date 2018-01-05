from IMSDBParser import IMSDBParser
import numpy as np


def read_name_file(filename):
    """Read a file containing a list of names
        Args:
            filename: a file containing a name for each row
        Returns:
            An array of names from the input file
    """
    names = []
    with open(filename, "r") as f:
        for line in f:
            if not line.startswith("#") and line.strip() != "":  # remove comments and empty lines
                names.append(line.strip().lower())
    return names


def baseline_bechdel_test(script):
    """Implements a baseline bechdel test which return True if two women are speaking
        Args:
            script: a parsed script from the IMSDBParser class
        Returns:
            Whether the test is passed
    """
    prev_speaker = None
    test_passed = False
    for speaker, line in script:
        if speaker in female_names:
            if prev_speaker != speaker and prev_speaker is not None: #two women are talking!
                test_passed = True
                break
            else:
                prev_speaker = speaker
        else:
            prev_speaker = None
    return test_passed


def complete_bechdel_test(script):
    """Implements the complete bechdel test
        Args:
            script: a parsed script from the IMSDBParser class
        Returns:
            Whether the test is passed
    """
    prev_speaker = None
    test_passed = False
    for speaker, line in script:
        if speaker in female_names: #woman talking
            if prev_speaker != speaker and prev_speaker is not None: #two women are talking...
                talking_about_men=False #are they talking about men?
                for name in male_names:
                    if name in line:
                        talking_about_men=True
                if talking_about_men:  # They're talking about men
                    test_passed = False
                else:  # They're not talking about men!
                    test_passed= True
            else:  # prev speaker was a male/this speaker
                prev_speaker = speaker
        else:  # if a woman-to-woman male-free discussion was completed, return True
            if test_passed==True:
                break
            else:
                prev_speaker = None
    return test_passed

female_names = "data/female.txt"
male_names = "data/male.txt"
male_names = read_name_file(male_names)
female_names = read_name_file(female_names)
parser = IMSDBParser(male_names+female_names, n_scripts=100)
scripts = parser.get_all_scripts()
#successful_movies = []  # this will store movies which passed the baseline test
complete_successful_movies = []  # this will store movies which passed the complete test
unsuccessful_movies = []  # this will store movies which didn't pass the complete test
for script in scripts:
    #if baseline_bechdel_test(script):
    #    successful_movies.append(script)
    if complete_bechdel_test(script):
        complete_successful_movies.append(script)
    else:
        unsuccessful_movies.append(script)
print "Bechdel Test completed!"
print "Parsed", len(scripts), "files!"
#print "Found", int(len(successful_movies)), "movies passing the Baseline Bechdel Test"
print "Found", int(len(complete_successful_movies)), "movies passing the Complete Bechdel Test"
#print "(", format(float(len(successful_movies))/len(scripts)*100, ".0f"), "% of movies for the baseline)"
print "(", format(float(len(complete_successful_movies))/len(scripts)*100, ".0f"), "% of movies for the complete test)"
print "Average number of lines for each script (successful/unsuccessful):"
print int(np.average([len(m) for m in complete_successful_movies])), int(np.average([len(m) for m in unsuccessful_movies]))
print "Average number of different characters for each script (successful/unsuccessful):"
print int(np.average([len(set([m[0] for m in movie])) for movie in complete_successful_movies])),\
    int(np.average([len(set([m[0] for m in movie])) for movie in unsuccessful_movies]))
print "Average number of male characters for each script (successful/unsuccessful):"
print int(np.average([len(set([m[0] for m in movie if m[0] in male_names])) for movie in complete_successful_movies])),\
    int(np.average([len(set([m[0] for m in movie if m[0] in male_names])) for movie in unsuccessful_movies]))
print "Average number of female characters for each script (successful/unsuccessful):"
print int(np.average([len(set([m[0] for m in movie if m[0] in female_names])) for movie in complete_successful_movies])),\
    int(np.average([len(set([m[0] for m in movie if m[0] in female_names])) for movie in unsuccessful_movies]))
