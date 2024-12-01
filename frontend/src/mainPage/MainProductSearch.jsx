import React, { useState, useEffect } from "react";
import { SearchBar } from "../components/SearchBar";
import styles from "./ProductSearch.module.css";
import ListProductCard from "../components/ListProductCard";
import { getAllProductIds } from "../API/localStorageUtils";
import ContentLoader from "react-content-loader";
import { fetchProducts } from "../API/api";

const MainProductSearch = () => {
	const [currentProduct, setCurrentProduct] = useState([]);
	const [loadingStatus, setLoadingStatus] = useState(true);

	useEffect(() => {
		const fetchData = async () => {
			const productIds = await getAllProductIds().reverse();
			const productsData = [];

			for (let temp of productIds) {
				const pop = await fetchProducts(temp);
				productsData.push(pop[0]);
			}

			setCurrentProduct(productsData);
			setLoadingStatus(false);
		};

		fetchData();
	}, []);

	const gridHistory = (
		<div className={styles.productGrid}>
			{currentProduct.map((product, index) => (
				<ListProductCard key={index} {...product} type="history" />
			))}
		</div>
	);

	const Skeleton = () => (
		<ContentLoader
			speed={2}
			width={504}
			height={430}
			viewBox="0 0 504 430"
			backgroundColor="#d3d3d3"
			foregroundColor="#e0e0e0"
			preserveAspectRatio="xMidYMid meet"
		>
			<rect x="0" y="0" rx="5" ry="5" width="504" height="430" />
		</ContentLoader>
	);

	const loading = (
		<div className={styles.skeletonGrid}>
			<Skeleton />
			<Skeleton />
			<Skeleton />
		</div>
	);

	const emptyHistory = <p className={styles.emptyMessage}>Нет данных</p>;

	return (
		<main className={styles.container}>
			<h1 className={styles.title}>сайтик МКЛП</h1>
			<SearchBar />
			<h1 className={styles.historyTitle}>История:</h1>
			<div className>
				{loadingStatus
					? loading
					: currentProduct.length > 0
					? gridHistory
					: emptyHistory}
			</div>
		</main>
	);
};

export default MainProductSearch;
