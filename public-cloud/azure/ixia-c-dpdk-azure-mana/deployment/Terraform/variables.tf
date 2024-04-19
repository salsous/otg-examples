variable "AgentVmSize" {
	default = "Standard_F8s_v2"
	description = "Category, series and instance specifications associated with the VM"
	type = string
	validation {
		condition = contains([	"Standard_F4s_v2",	"Standard_F8s_v2",	"Standard_F16s_v2",
								"Experimental_Boost4", "Experimental_Boost8", "Experimental_Boost32", "Experimental_Boost64", "Experimental_Boost192"
							], var.AgentVmSize)
		error_message = <<EOF
AgentVmSize must be one of the following sizes:
	Standard_F4s_v2, Standard_F8s_v2, Standard_F16s_v2,
	Experimental_Boost4, Experimental_Boost8, Experimental_Boost32, Experimental_Boost64, Experimental_Boost192
		EOF
	}
}

variable "PublicSecurityRuleSourceIpPrefixes" {
	description = "List of IP Addresses /32 or IP CIDR ranges connecting inbound to App"
	type = list(string)
}

variable "ResourceGroupLocation" {
	default = "South Central US"
	type = string
}

variable "ResourceGroupName" {
	type = string
}

variable "SubscriptionId" {
	sensitive = true
	type = string
}

variable "UserEmailTag" {
	description = "Email address tag of user creating the deployment"
	type = string
}

variable "UserLoginTag" {
	description = "Login ID tag of user creating the deployment"
	type = string
}

variable "UserProjectTag" {
	default = "cloud-ist"
	type = string
}