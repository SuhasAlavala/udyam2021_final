import gspread
from oauth2client.service_account import ServiceAccountCredentials
from authentication.models import User

def addtosheet(sheetname, teamslist):
	scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
	creds = ServiceAccountCredentials.from_json_keyfile_name("udyam_backend/creds.json", scope)
	client = gspread.authorize(creds)
	sheet = client.open(sheetname).sheet1

	sheet.delete_rows(2, sheet.row_count)
	sheet.append_row(["-", "-", "-", "-", "-", "-", "-", "-"])

	i=1
	for team in teamslist:
		try:
			leader = User.objects.get(email=team.Team_leader)
		except:
			leader = None
		try:
			member1 = User.objects.get(email=team.member1)
		except:
			member1 = None
		try:
			member2 = User.objects.get(email=team.member2)
		except:
			member2 = None


		if member2:
			row = [str(i), team.team_name, "", leader.first_name, "", member1.first_name, "", member2.first_name]
			sheet.append_row(row)
			row = [" ", " ", " ", leader.email, "", member1.email, "", member2.email]
			sheet.append_row(row)
			row = [" ", " ", " ", leader.Phone, "", member1.Phone, "", member2.Phone]
			sheet.append_row(row)
		elif member1:
			row = [str(i), team.team_name, "", leader.first_name, "", member1.first_name, "", "None"]
			sheet.append_row(row)
			row = [" ", " ", " ", leader.email, "", member1.email, "", "None"]
			sheet.append_row(row)
			row = [" ", " ", " ", leader.Phone, "", member1.Phone, "", "None"]
			sheet.append_row(row)
		elif leader:
			row = [str(i), team.team_name, "", leader.first_name, "", "None", "", "None"]
			sheet.append_row(row)
			row = [" ", " ", " ", leader.email, "", "None", "", "None"]
			sheet.append_row(row)
			row = [" ", " ", " ", leader.Phone, "", "None", "", "None"]
			sheet.append_row(row)

		sheet.append_row(["-", "-", "-", "-", "-", "-", "-", "-"])
		i = i+1