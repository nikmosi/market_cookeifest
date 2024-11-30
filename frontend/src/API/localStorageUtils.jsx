const LOCAL_STORAGE_KEY = "productIds";

export const addProductId = (id) => {
	if (!id) return;

	const storedIds = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY)) || [];

	storedIds.push(id);

	localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(storedIds));
};

export const getAllProductIds = () => {
	return JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY)) || [];
};

export const getLastProductId = () => {
	const storedIds = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY)) || [];
	return storedIds.length > 0 ? storedIds[storedIds.length - 1] : null;
};
