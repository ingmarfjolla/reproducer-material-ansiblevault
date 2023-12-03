from github import Github, Auth
from dotenv import load_dotenv
import os
import csv

def search_github(keywords, directory):
    result = g.search_code(keywords)
    print(result.totalCount)
    count = 0
    for repo in result:
        count += 1
        # print(repo.html_url)
        print("{} file(s) searched.".format(count))
        if ".md" in repo.html_url or ".rst" in repo.html_url:
            print("ignoring file")
            continue
        else:
            trimmed_repo_name = repo.html_url[repo.html_url.index(".com/") + len(".com/"):]
            trimmed_repo_name = trimmed_repo_name[:trimmed_repo_name.index("/blob")].replace("/", ".")
            filename = "{count}_{user_and_repository}.txt".format(count=count,user_and_repository=trimmed_repo_name) 
            f = open(directory + "/" + filename, "w")
            f.write(str(repo.html_url)+'\n')
            f.write(repo.decoded_content.decode()+'\n')

def find_vault_id(directory):
    total_vaults=0
    total_vault_id=0
    for file in os.listdir(directory):
        if file.endswith(".txt"):
            
            f = open(path + "/" + file, "r")
            count = 0
            for line in f:
                count += 1
                if "$ANSIBLE_VAULT;1.2;AES256" in line:
                    total_vaults+=1
                if "$ANSIBLE_VAULT;1.2;AES256;" in line:
                    total_vault_id+=1
                    print("Vault ID at line {} in file {}: {}".format(
                        count, f.name, line[line.index("AES256;") + len("AES256;"):].split()
                    ))
    print("total vaults: "+str(total_vaults))
    print("total vault ids: "+str(total_vault_id))
def find_vault_issues():
  
    with open('vault_issues.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Number","Title", "Body", "Comments", "Labels","State","CreatedDate"])

        issues = g.search_issues(query="vault repo:ansible/ansible type:issue")
        for issue in issues:
            labels = ', '.join([label.name for label in issue.labels])
            comments = ' | '.join([comment.body.replace('\n', ' ').replace('\r', '') for comment in issue.get_comments()])
            writer.writerow([issue.number,issue.title, issue.body.replace('\n', ' ').replace('\r', ''), comments, labels,issue.state,issue.created_at])

if __name__ == "__main__":
    # load env and connect to gh
    load_dotenv()
    GITHUB_PAT = os.getenv("GITHUB_PAT")
    auth = Auth.Token(GITHUB_PAT)
    g = Github(auth=auth)

    # create directory
    path = "./files"
    if not os.path.exists(path):
        os.mkdir(path)

    #search_github("$ANSIBLE_VAULT;1.2;AES256", path)
    #find_vault_id(path)
    find_vault_issues()