// api.js
import axios from "axios";

const host = import.meta.env.VITE_APP_HOST;
console.log(host);

const api = axios.create({
	baseURL: host ? host : "",
	headers: {
		"Content-Type": "application/json",
	},
});

export const fetchProducts = async (article) => {
	try {
		const response = await api.get(`/api/products/${article}`);
		return response.data;
	} catch (error) {
		console.error("Error fetching products:", error);
	}
};

export const fetchArticles = async (article) => {
	try {
		const response = await api.get(`/api/products/${article}/similar`);
		return response.data;
	} catch (error) {
		console.error("Error fetching articles:", error);
	}
};

api.interceptors.response.use(
	(response) => response,
	(error) => {
		console.error("API Error:", error.response || error.message);
		return Promise.reject(error);
	}
);

export default api;
