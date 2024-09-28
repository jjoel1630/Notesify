// import
import React from "react";
import Dashboard from "views/Dashboard/Dashboard.js";
import Tables from "views/Dashboard/Tables.js";
import Billing from "views/Dashboard/Billing.js";

import { HomeIcon, StatsIcon, CreditIcon } from "components/Icons/Icons";

var dashRoutes = [
	{
		path: "audionote",
		name: "New Note",
		icon: <HomeIcon color="inherit" />,
		component: Dashboard,
		layout: "/",
		fileId: "",
		audioId: "",
	},
	{
		path: "1",
		name: "[filename1]",
		icon: <HomeIcon color="inherit" />,
		component: Dashboard,
		layout: "/",
		fileId: "1",
		audioId: "1",
	},
	{
		path: "2",
		name: "[filename2]",
		icon: <HomeIcon color="inherit" />,
		component: Dashboard,
		layout: "/",
		fileId: "2",
		audioId: "2",
	},
];
export default dashRoutes;
