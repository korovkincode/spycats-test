'use client';
import { useState, useEffect, useRef, FormEvent } from 'react';
import { SpyCat } from './types/spy-cat';
import { Container, Box, Typography, IconButton, Grid, Skeleton, Card, CardContent, CardHeader, Modal, TextField, Button } from '@mui/material';
import { Add, Delete, Edit, Done, Cancel } from '@mui/icons-material';
import { addCat, deleteCat, getAllCats, updateCat } from './API/spy-cat';

export default function Home() {
	const [formOpen, setFormOpen] = useState<boolean>(false);
	const [formData, setFormData] = useState<SpyCat>({
		ID: null, name: '', experience: 0,
		breed: '', salary: 0
	});
	const [editingSalary, setEditingSalary] = useState<string>('');
	const [editedSalary, setEditedSalary] = useState<number>(0);
	const [catsData, setCatsData] = useState<SpyCat[] | null>(null);
	const [dataLoaded, setDataLoaded] = useState<boolean>(false);

	useEffect(() => {
		const fetchCats = async () => {
			const catsRequest = await getAllCats();
            if (catsRequest.status !== 200) {
                throw new Error(catsRequest.description);
            }
            setCatsData(catsRequest.data);
			setDataLoaded(true);
		};

		fetchCats();
	}, []);

	const removeCat = async (catID: string) => {
		const catRequest = await deleteCat(catID);
		if (catRequest.status !== 200) {
			throw new Error(catRequest.description);
		}

		let newCataData = [];
		for (const catData of catsData || []) {
			if (catData.ID !== catID) {
				newCataData.push(catData);
			}
		}
		setCatsData(newCataData);
	};

	const editCat = async (catID: string) => {
		const catRequest = await updateCat({
			catID: catID, salary: editedSalary
		});
		if (catRequest.status !== 200) {
			throw new Error(catRequest.description);
		}

		let newCataData = [];
		for (const catData of catsData || []) {
			if (catData.ID === catID) {
				catData.salary = editedSalary;
			}
			newCataData.push(catData);
		}
		setCatsData(newCataData);
		setEditingSalary('');
	};

	const handleForm = async (e: FormEvent) => {
		e.preventDefault();
		const catRequest = await addCat(formData);
		if (catRequest.status !== 200) {
			throw new Error(catRequest.description);
		}

		setCatsData((catsData || []).concat([catRequest.data]));
		setFormOpen(false);
	};

	return (
		<>
			<Container maxWidth="md">
				<Box sx={{ mt: '50px', display: 'flex', justifyContent: 'space-between' }}>
					<Typography sx={{ fontSize: '24px', fontWeight: 700 }}>
						Spy Cat Agency 🕵️
					</Typography>
					<IconButton sx={{ color: '#2ac91e' }} onClick={() => setFormOpen(true)}>
						<Add />
					</IconButton>
				</Box>
				<Grid container spacing={2} sx={{ mt: 5 }}>
					{dataLoaded
					?
						catsData?.map((cat, index) =>
							<Grid size={{ xs: 12, md: 4 }} key={index}>
								<Card sx={{ border: '1px solid #2ac91e', borderRadius: 3 }}>
									<CardHeader
										title={cat.name} subheader={`${cat.breed} breed`}
										action={
											<IconButton sx={{ color: '#eb021a' }} onClick={() => removeCat(cat.ID || '')}>
												<Delete />
											</IconButton>
										}
										slotProps={{
											title: {fontSize: 24, fontWeight: 700},
											subheader: {fontSize: 14, fontWeight: 300}
										}}
									/>
									<CardContent sx={{ mt: -2 }}>
										<Typography>
											{cat.experience} years of experience
										</Typography>
										<Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
											{editingSalary === cat.ID
											?
												<>
													<TextField
														sx={{ mt: 2 }} required
														value={editedSalary} type="number"
														onChange={e => setEditedSalary(Number(e.target.value))}
														fullWidth label="Cat salary"
														placeholder="Enter cat salary (in USD)"
													/>
													<IconButton sx={{ mr: -1, color: '#2ac91e' }} onClick={() => editCat(cat.ID || '')}>
														<Done />
													</IconButton>
													<IconButton sx={{ mr: -1, color: '#eb021a' }} onClick={() => setEditingSalary('')}>
														<Cancel />
													</IconButton>
												</>
											:
												<>
													<Typography sx={{ mt: 2, fontSize: '18px', fontWeight: 700 }}>
														{cat.salary}$
													</Typography>
													<IconButton sx={{ mr: -1 }} onClick={() => setEditingSalary(cat.ID || '')}>
														<Edit />
													</IconButton>
												</>
											}
										</Box>
									</CardContent>
								</Card>
							</Grid>
						)
					:
						Array(18).fill(0).map((_, index) =>
							<Grid size={{ xs: 12, md: 4 }} key={index}>
								<Skeleton
									variant="rectangular" 
									sx={{ 
										width: '100%', height: {xs: '100vw', md: '15vw'}
									}}
								/>
							</Grid>
						)
					}
				</Grid>
			</Container>
			<Modal
				open={formOpen}
				onClose={() => setFormOpen(false)}
			>
				<Box sx={{
					position: 'absolute',
					top: '50%',
					left: '50%',
					transform: 'translate(-50%, -50%)',
					width: 400,
					bgcolor: 'background.paper',
					border: '2px solid #000',
					boxShadow: 24,
					p: 4,
				}}>
					<Box component="form" noValidate sx={{ mt: 3 }}>
						<Grid container spacing={2} alignItems="center">
							<Typography sx={{ fontSize: '30px', fontWeight: 700 }}>
								New Cat
							</Typography>
							<Grid size={{ xs: 12 }}>
								<TextField
									required value={formData.name}
									onChange={e => setFormData({...formData, name: e.target.value})}
									fullWidth label="Cat name"
									placeholder="Enter cat name"
								/>
							</Grid>
							<Grid size={{ xs: 12 }}>
								<TextField
									required value={formData.experience} type="number"
									onChange={e => setFormData({...formData, experience: Number(e.target.value)})}
									fullWidth label="Cat experience"
									placeholder="Enter cat experience (in years)"
								/>
							</Grid>
							<Grid size={{ xs: 12 }}>
								<TextField
									required value={formData.breed}
									onChange={e => setFormData({...formData, breed: e.target.value})}
									fullWidth label="Cat breed"
									placeholder="Enter cat breed"
								/>
							</Grid>
							<Grid size={{ xs: 12 }}>
								<TextField
									required value={formData.salary} type="number"
									onChange={e => setFormData({...formData, salary: Number(e.target.value)})}
									fullWidth label="Cat salary"
									placeholder="Enter cat salary (in USD)"
								/>
							</Grid>
						</Grid>
						<Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }} onClick={handleForm}>
							Add
						</Button>
					</Box>
				</Box>
			</Modal>
		</>
	);
}
