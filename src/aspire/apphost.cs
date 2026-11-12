
//Packages
#:package Aspire.Hosting.AppHost@17.1.0-preview.1.26561.12
#:package Aspire.Hosting.Azure.CosmosDB@17.1.0-preview.1.26561.12
#:package Aspire.Hosting.Azure.Network@17.1.0-preview.1.26561.12
#:package Aspire.Hosting.Azure.Sql@17.1.0-preview.1.26561.12
#:package Aspire.Hosting.Azure.Storage@17.1.0-preview.1.26561.12
#:package Aspire.Hosting.Foundry@17.1.0-preview.1.26561.12
#:package Aspire.Hosting.Python@17.1.0-preview.1.26561.12

using Aspire.Hosting.Azure;
using Aspire.Hosting.Foundry;

var builder = DistributedApplication.CreateBuilder(args);

// Networking setup
#pragma warning disable ASPIREAZURE003
var vnet = builder.AddAzureVirtualNetwork("vnet-expenses-swe");
var subnet = vnet.AddSubnet("pe-subnet","10.0.0.0/24");

var foundry = builder.AddFoundry("foundry-expenses-swe");
var foundryProject = foundry.AddProject("demo");
var chatModel = foundryProject.AddModelDeployment("gpt-5", FoundryModel.OpenAI.Gpt5);

// Cosmos DB: conversation transcripts
var cosmos = builder.AddAzureCosmosDB("cosmos-agent-history-swe");

const string ConversationsContainer = "conversations";

var database = cosmos.AddCosmosDatabase("conversation-history");
database.AddContainer(ConversationsContainer, "/userId");

// Azure Blob Storage for receipts
var storage = builder.AddAzureStorage("expensesreceiptsimages");
var receiptImages = storage.AddBlobContainer("receipt-images");

// SQL DATABASE for storing expenses records
var sql = builder.AddAzureSqlServer("sql-server-expenses-swe");
var fb = sql.AddDatabase("expenses-db");

builder.Build().Run();
