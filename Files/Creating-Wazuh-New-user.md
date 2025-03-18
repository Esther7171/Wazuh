## Creating and setting a Wazuh admin user

1. Log into the Wazuh dashboard as administrator.
2. Click the upper-left menu icon ☰ to open the options, go to Indexer management > Security, and then Internal users to open the internal users' page.
![internal-user1](https://github.com/user-attachments/assets/5be0f396-4f58-478c-904a-42d5d74b0cf6)

3. Click Create internal user, provide a username and password, and click Create to complete the action.
4. To map the user to the admin role, follow these steps:
  * Click the upper-left menu icon ☰ to open the options, go to Indexer management > Security, and then Roles to open the roles page.
  * Search for the all_access role in the roles list and select it to open the details window.
  * Click Duplicate role, assign a name to the new role, then click Create to confirm the action.
  * Select the newly created role.
  * Select the Mapped users tab and click Manage mapping.
  * Add the user you created in the previous steps and click Map to confirm the action.

> Note: Reserved roles are restricted for any permission customizations. You can create a custom role with the same permissions or duplicate a reserved role for further customization.


