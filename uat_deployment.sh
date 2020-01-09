USERNAME=lh-admin-tax
PASSWORD=Kpmg1234$

echo -e "$BACKEND\tPushing to backend..."
git push https://$USERNAME:$PASSWORD@itra-backend-uat.scm.azurewebsites.net:443/itra-backend-uat.git HEAD:master

sleep 1
echo -e "$FROTEND\tPushing to Front End. Please ensure that the folder is on the same level as backend and NPM is installed"
sleep 1
cd ../itra
npm run build
az storage blob upload-batch --destination '$web' --account-name itrafrontenduat --account-key rYhbloa4MpJTpE3EF3TbmW7DcE8iYB7S5jq3Hq2AQlRBuW02avtQRkFhEQEdgE1B62fsItB+z80LSQB18mXUDw== -s dist
