import React, { useState, useEffect } from "react";
import { SearchBar } from "../components/SearchBar";
import styles from "./ProductSearch.module.css";
import ListProductCard from "../components/ListProductCard";
import { getAllProductIds } from "../API/localStorageUtils";
import { fetchProducts } from "../API/api";

const MainProductSearch = () => {
	const [currentProduct, setCurrentProduct] = useState([]);

	useEffect(() => {
		const fetchData = async () => {
			const productIds = await getAllProductIds();
			const productsData = [];

			// Загружаем данные по каждому продукту и добавляем в массив
			for (let temp of productIds) {
				const pop = await fetchProducts(temp);
				productsData.push(pop[0]); // Добавляем первый продукт, предполагается, что pop - это массив
			}

			// Обновляем состояние с полученными данными
			setCurrentProduct(productsData);
		};

		fetchData(); // Вызов асинхронной функции
	}, []); // Пустой массив зависимостей, чтобы выполнить эффект один раз при монтировании компонента

	const grid = (
		<div className={styles.productGrid}>
			{currentProduct.map((product, index) => (
				<ListProductCard key={index} {...product} />
			))}
		</div>
	);

	return (
		<main className={styles.container}>
			<h1 className={styles.title}>сайтик МКЛП</h1>
			<SearchBar />
			{currentProduct && currentProduct.length > 0 ? grid : <p>Поиск...</p>}
		</main>
	);
};

export default MainProductSearch;
