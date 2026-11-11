//Packages
#:package Aspire.Hosting.AppHost@13.6.4
#:package Aspire.Hosting.Azure.CosmosDB@13.6.4
#:package Aspire.Hosting.Azure.Storage@13.6.4
#:package Aspire.Hosting.Foundry@13.5.3-preview.1.26425.3
#:package Aspire.Hosting.JavaScript@13.6.4
#:package Aspire.Hosting.Python@13.6.4
#:package Aspire.Hosting.SqlServer@13.6.4
#:package CommunityToolkit.Aspire.Hosting.PowerShell@13.6.1

//Sdks
#:sdk Aspire.AppHost.Sdk@13.6.4

// The file-based AppHost intentionally does not use the Aspire CLI bundle.
#:property NoWarn=ASPIRE010

using Aspire.Hosting;
using Aspire.Hosting.ApplicationModel;
using Aspire.Hosting.Foundry;
using Azure.Provisioning.Storage;
using System.Management.Automation;

var builder = DistributedApplication.CreateBuilder(args);

var existingFoundryName = builder.AddParameter("existingFoundryName");

var foundry = builder.AddFoundry("foundry").AsExisting(existingFoundryName, resourceGroupParameter: null);

var foundryProject = foundry.AddProject("expenses");

var chatModel = foundryProject.AddModelDeployment("gpt-5", FoundryModel.OpenAI.Gpt5);
// The default 1,000 TPM cannot cover a receipt plus the agent's tool schemas.
chatModel.Resource.SkuCapacity = 100;

// Cosmos DB: conversation transcripts
var cosmos = builder.AddAzureCosmosDB("cosmos-conversation-history");

const string ConversationsContainer = "conversations";

var database = cosmos.AddCosmosDatabase("conversation-history");
database.AddContainer(ConversationsContainer, "/userId");

// Azure Blob Storage for receipts
var storage = builder.AddAzureStorage("storage-receipts");
var receiptImages = storage.AddBlobContainer("receipt-images");

// SQL SERVER for storing expenses records
var sqlServer = builder.AddSqlServer("sql-server-records");
var db = sqlServer.AddDatabase("records-db");

builder.Build().Run();
