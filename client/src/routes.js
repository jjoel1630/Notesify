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
	},
	{
		path: "audionote/1",
		name: "[filename]",
		icon: <HomeIcon color="inherit" />,
		component: Dashboard,
		layout: "/",
		fileId: "1",
		audioId: "1",
	},
	{
		path: "audionote/2",
		name: "[filename]",
		icon: <HomeIcon color="inherit" />,
		component: Dashboard,
		layout: "/",
		fileId: "1",
		audioId: "1",
	},
];
export default dashRoutes;
