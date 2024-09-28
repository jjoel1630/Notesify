// Chakra imports
import {
	Box,
	Button,
	Flex,
	Grid,
	Progress,
	SimpleGrid,
	Stat,
	StatLabel,
	StatNumber,
	Table,
	Tbody,
	Td,
	Text,
	Th,
	Thead,
	Tr,
	useColorMode,
	useColorModeValue,
} from "@chakra-ui/react";
// Custom components
import Card from "components/Card/Card.js";
import BarChart from "components/Charts/BarChart";
import LineChart from "components/Charts/LineChart";
import IconBox from "components/Icons/IconBox";
// Custom icons
import { CartIcon, DocumentIcon, GlobeIcon, WalletIcon } from "components/Icons/Icons.js";
import React, { useEffect } from "react";
// Variables
import { barChartData, barChartOptions, lineChartData, lineChartOptions } from "variables/charts";
import { pageVisits, socialTraffic } from "variables/general";

export default function Dashboard(props) {
	// useEffect(() => {
	// 	console.log("Props updated:", props);
	// }, [props.fileID, props.audioID, props.fileName, props.customProp]);

	// Chakra Color Mode
	const iconBlue = useColorModeValue("blue.500", "blue.500");
	const iconBoxInside = useColorModeValue("white", "white");
	const textColor = useColorModeValue("gray.700", "white");
	const tableRowColor = useColorModeValue("#F7FAFC", "navy.900");
	const borderColor = useColorModeValue("gray.200", "gray.600");
	const textTableColor = useColorModeValue("gray.500", "white");

	const { colorMode } = useColorMode();

	return (
		<>
			<div>{props.fileID}</div>
			<div>{props.audioID}</div>
			<div>{props.fileName}</div>
			<div>{props.customProp}</div>
		</>
	);
}
