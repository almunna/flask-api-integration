const msalConfig = {
  auth: {
    clientId: "YOUR_CLIENT_ID",
    authority: "https://login.microsoftonline.com/YOUR_TENANT_ID",
    redirectUri: "http://localhost:3000"
  }
};

const msalInstance = new msal.PublicClientApplication(msalConfig);

msalInstance.loginPopup({
  scopes: ["Team.ReadBasic.All"]
}).then(response => {
  const token = response.accessToken;
  fetch("/api/teams/user-joined", {
    headers: {
      Authorization: `Bearer ${token}`
    }
  }).then(res => res.json()).then(console.log);
});
