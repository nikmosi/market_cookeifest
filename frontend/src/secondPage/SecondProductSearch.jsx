// SecondProductSearch.jsx
import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import styles from "./SecondProductSearch.module.css";
import ListProductCard from "../components/ListProductCard";
import { ProductCard } from "../components/ProductCard";
import { getLastProductId } from "../API/localStorageUtils";
import { fetchProducts, fetchArticles } from "../API/api";

const SecondProductSearch = () => {
	const [products, setProducts] = useState(null);
	const [currentProduct, setCurrentProduct] = useState([]);

	useEffect(() => {
		const fetchData = async () => {
			const lastProduct = getLastProductId();
			if (lastProduct) {
				const fetchedData = await fetchProducts(lastProduct);
				setProducts(fetchedData[0]);
				console.log("Fetched data:", fetchedData);
			}
		};
		const fetchArtic = async () => {
			const articles = getLastProductId();
			if (articles) {
				const fetchedData = await fetchArticles(articles);
				for (let temp of fetchedData.articles.slice(0, 3)) {
					const pop = await fetchProducts(temp);
					setCurrentProduct((prevProducts) => [...prevProducts, pop[0]]);
				}

				console.log(" data:", currentProduct);
			}
		};
		fetchData();
		fetchArtic();
	}, []);

	const grid = (
		<div className={styles.productGrid}>
			{currentProduct.map((currentProduct, index) => (
				<ListProductCard key={index} {...currentProduct} />
			))}
		</div>
	);
	return (
		<main className={styles.container}>
			<div className={styles.header}>
				<Link to="/" className={styles.backButton}>
					<button>НА ГЛАВНУЮ </button>
				</Link>
				<h2 className={styles.pageTitle}>Ваш товар</h2>
			</div>

			<div className={styles.productCardContainer}>
				<ProductCard {...products} />
			</div>

			<section className={styles.productsSection}>
				<div className={styles.sort}>
					<span className={styles.analog}>Аналогичные товары</span>
					<button>Сортировать</button>
				</div>
				{currentProduct && currentProduct.length > 0 ? grid : <p>Поиск...</p>}
			</section>
		</main>
	);
};

export default SecondProductSearch;
