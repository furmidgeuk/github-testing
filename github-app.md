1. Create a Github app in your organization
2. Set the necessary permissions to it and generate a PEM
3. Install the app in your organisation
4. Store its PEM in GitHub secrets as `GH_PRIVATE_KEY` 
5. Store the Github App Id in Github secrets as `GH_APP_ID`

```
Use the code here:
checkout-other-repo:
    runs-on: ubuntu-latest
    steps:
      - name: Get Token
        id: get_workflow_token
        uses: actions/create-github-app-token@v1
        with:
          app-id: ${{ secrets.GH_APP_ID  }}
          private-key: ${{ secrets.GH_PRIVATE_KEY }} 
          owner: ${{ github.repository_owner }}
      - name: Checkout
        uses: actions/checkout@v4        
        with:
          token: ${{ steps.get_workflow_token.outputs.token }}
          repository: ...
```

- GitHub Apps authenticate using a private key (PEM file) that is used to generate a JWT (JSON Web Token).
- This JWT is then exchanged for an installation access token that provides scoped permissions.
- The GitHub Actions runner and gh CLI both support using the raw PEM format without requiring base64 encoding.
