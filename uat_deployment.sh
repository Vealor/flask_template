USERNAME=lh-admin-tax
PASSWORD=Kpmg1234$
sleep 1 && echo -e "\tChecking if Azure remote URL exists" && sleep 1
AZURE_EXISTS=$(git remote -v | grep azure)

if [ ${#AZURE_EXISTS} -gt 1 ]; then
  echo -e "$BACKEND\tAzure Remote Exists. Pushing to backend..."
  git push https://$USERNAME:$PASSWORD@itra-backend-uat.scm.azurewebsites.net:443/itra-backend-uat.git HEAD:master
else
  echo -e "$BACKEND\tAzure Remote Does not exist. Adding remote URL and pushing to backend."
  git push remote add azure https://$USERNAME:$PASSWORD@itra-backend-uat.scm.azurewebsites.net:443/itra-backend-uat.git
  git push azure HEAD:master
fi

sleep 1
echo -e "$FROTEND\tPushing to Front End. Please ensure that the folder is on the same level as backend and NPM is installed"
sleep 1
cd ../itra
npm run build
az storage blob upload-batch --destination '$web' --account-name itrafrontenduat --account-key rYhbloa4MpJTpE3EF3TbmW7DcE8iYB7S5jq3Hq2AQlRBuW02avtQRkFhEQEdgE1B62fsItB+z80LSQB18mXUDw== -s dist
