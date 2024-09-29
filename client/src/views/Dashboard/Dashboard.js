import { HomeIcon } from "components/Icons/Icons";
import React, { useEffect, useState } from "react";
import dashRoutes from "routes";
import { useHistory } from "react-router-dom";

export default function Dashboard(props) {
	const [audioUrl, setAudioUrl] = useState(null);
	const [audioError, setAudioError] = useState(null);
	const [isUploaded, setIsUploaded] = useState(true);
	const [file, setFile] = useState(null);
	const [fileError, setFileError] = useState(null);
	const [success, setSuccess] = useState(null);

	const history = useHistory();

	useEffect(() => {
		const fetchAudioByte = async () => {
			console.log(props);
			if (props.fileID === "") {
				setIsUploaded(false);
				return;
			}
			console.log("fetchaudio");

			try {
				const response = await fetch(
					`http://127.0.0.1:5000/api/get_audio_byte?file_id=${props.audioID}`,
					{
						method: "GET",
					}
				);
				if (!response.ok) {
					throw new Error("Network response was not ok");
				}
				const data = await response.json();
				console.log(data);
				if (data.audio) {
					const audioBlob = await fetch(`data:audio/wav;base64,${data.audio}`); // Adjust MIME type as needed
					const blobUrl = URL.createObjectURL(await audioBlob.blob());
					setAudioUrl(blobUrl); // Set the audio URL for the <audio> element
				} else {
					console.log("getAudioRes");
					try {
						const getAudioRes = await fetch("http://127.0.0.1:5000/api/get_audio_id", {
							method: "POST",
							headers: {
								"Content-Type": "application/json",
							},
							body: JSON.stringify({
								file_id: fileId,
								duration: duration,
							}),
						});

						if (!getAudioRes.ok) {
							const errorData = await response.json();
							throw new Error(errorData.error || "Something went wrong");
						}

						const result = await getAudioRes.json();
						const getAudioByteRes = await fetch(
							`http://127.0.0.1:5000/api/get_audio_byte?file_id=${result.document_id}`,
							{
								method: "GET",
							}
						);
						if (!getAudioByte.ok) {
							throw new Error("Network response was not ok");
						}
						const getAudioByteData = await getAudioByteRes.json();

						const getAudioBlob = await fetch(
							`data:audio/wav;base64,${getAudioByteData.audio}`
						); // Adjust MIME type as needed
						const getAudioBlobUrl = URL.createObjectURL(await getAudioBlob.blob());
						setAudioUrl(getAudioBlobUrl); // Set the audio URL for the <audio> element
					} catch (error) {
						console.log("error creating speech");
					}
				}
			} catch (error) {
				setAudioError(`Error fetching audio byte: ${error.message}`);
			}
		};

		fetchAudioByte();
	}, []);

	const retrieveAudio = async (fileId, duration) => {
		try {
			const getAudioRes = await fetch("http://127.0.0.1:5000/api/get_audio_id", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({
					file_id: fileId,
					duration: duration,
				}),
			});

			if (!getAudioRes.ok) {
				const errorData = await response.json();
				throw new Error(errorData.error || "Something went wrong");
			}

			const result = await getAudioRes.json();
			const getAudioByteRes = await fetch(
				`http://127.0.0.1:5000/api/get_audio_byte?file_id=${result.document_id}`,
				{
					method: "GET",
				}
			);
			if (!getAudioByteRes.ok) {
				throw new Error("Network response was not ok");
			}
			const getAudioByteData = await getAudioByteRes.json();

			const getAudioBlob = await fetch(`data:audio/wav;base64,${getAudioByteData.audio}`); // Adjust MIME type as needed
			const getAudioBlobUrl = URL.createObjectURL(await getAudioBlob.blob());
			setAudioUrl(getAudioBlobUrl); // Set the audio URL for the <audio> element
		} catch (error) {
			console.log(error);
		}
	};

	const handleFileChange = (event) => {
		const selectedFile = event.target.files[0];
		const allowedTypes = ["application/pdf", "text/plain", "application/x-latex", "image/jpeg"];

		// Check file type
		if (selectedFile && !allowedTypes.includes(selectedFile.type)) {
			setFileError("Please upload a valid file (PDF, TXT, LaTeX, JPG).");
			setFile(null);
		} else {
			setFile(selectedFile);
			setFileError(null);
		}
	};

	const handleUpload = async () => {
		if (!file) {
			setError("Please select a file to upload.");
			return;
		}

		// Convert file to base64
		const reader = new FileReader();
		reader.onloadend = async () => {
			const base64data = reader.result.split(",")[1]; // Get base64 string without the prefix

			try {
				const response = await fetch("http://127.0.0.1:5000/api/upload_file", {
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						name: file.name,
						type: file.type.split("/")[1],
						file_bin: base64data, // Send the base64 string
					}),
				});

				if (!response.ok) {
					const errorData = await response.json();
					throw new Error(errorData.error || "Something went wrong");
				}

				const result = await response.json();
				setSuccess(`File uploaded successfully! ID: ${result.id}`);
				setFileError(null);
				setFile(null); // Clear the file input

				await retrieveAudio(result.id, 2);

				// const fileData = {
				// 	path: result.id,
				// 	name: file.name,
				// 	component: "dashboard",
				// 	layout: "/",
				// 	fileId: result.id,
				// 	audioId: "",
				// };

				// Retrieve existing files from local storage
				// const existingFiles = JSON.parse(localStorage.getItem("uploadedFiles")) || [
				// 	dashRoutes[0],
				// ];

				// Add the new file data to the existing array
				// existingFiles.push(fileData);

				// Store the updated array back into local storage
				// localStorage.setItem("uploadedFiles", JSON.stringify(existingFiles));

				// history.push(`/${fileData.fileId}`);
			} catch (error) {
				setFileError(`Error uploading file: ${error.message}`);
				setSuccess(null);
			}
		};

		// Read the file as a data URL (base64)
		reader.readAsDataURL(file);
	};

	return (
		<div>
			<div>
				<input type="file" accept=".pdf,.txt,.tex,.jpg" onChange={handleFileChange} />
				<button onClick={handleUpload}>Upload</button>
				{/* <h1>{isUploaded ? "yes" : "no"}</h1>
				<h1>{audioUrl ? "yes" : "no"}</h1> */}
				{fileError && <p style={{ color: "red" }}>{fileError}</p>}
				{success && <p style={{ color: "green" }}>{success}</p>}
			</div>
			{audioUrl && (
				<audio controls>
					<source src={audioUrl} type="audio/wav" />
				</audio>
			)}
			{isUploaded && !audioUrl && <p>Loading audio...</p>}
		</div>
	);
}
