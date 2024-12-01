// SecondProductSearch.jsx
import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import styles from "./SecondProductSearch.module.css";
import ListProductCard from "../components/ListProductCard";
import { ProductCard } from "../components/ProductCard";
import { getLastProductId } from "../API/localStorageUtils";
import { fetchProducts, fetchArticles } from "../API/api";
import ContentLoader from "react-content-loader";
import { ClipLoader } from "react-spinners";
import Select from "react-select";

const SecondProductSearch = () => {
	const [products, setProducts] = useState(null);
	const [currentProduct, setCurrentProduct] = useState([]);
	const [loadingStatus, setLoadingStatus] = useState(true);
	const [loadingStatusBasicProduct, setLoadingStatusBasicProduct] =
		useState(true);

	useEffect(() => {
		const fetchData = async () => {
			const lastProduct = getLastProductId();
			if (lastProduct) {
				const fetchedData = await fetchProducts(lastProduct);
				setProducts(fetchedData[0]);
				setLoadingStatusBasicProduct(false);
			}
		};
		const fetchArtic = async () => {
			const articles = getLastProductId();
			if (articles) {
				const fetchedData = await fetchArticles(articles);
				for (let temp of fetchedData.articles.slice(0, 9)) {
					const pop = await fetchProducts(temp);
					setCurrentProduct((prevProducts) => [...prevProducts, pop[0]]);
				}

				console.log(" data:", currentProduct);
				setLoadingStatus(false);
			}
		};
		fetchData();
		fetchArtic();
	}, []);

	const Skeleton = () => (
		<ContentLoader
			speed={2}
			width={1780}
			height={500}
			viewBox="0 0 1780 500"
			backgroundColor="#d3d3d3"
			foregroundColor="#e0e0e0"
			preserveAspectRatio="xMidYMid meet"
		>
			<rect x="0" y="0" rx="5" ry="5" width="1780" height="500" />
		</ContentLoader>
	);

	const grid = (
		<div className={styles.productGrid}>
			{currentProduct.map((currentProduct, index) => (
				<ListProductCard key={index} {...currentProduct} />
			))}
		</div>
	);

	const options = [
		{ value: "price", label: "По цене" },
		{ value: "delivery", label: "По дате" },
		{ value: "rating", label: "по рейтингу" },
		{ value: "reviews_count", label: "по отзывам" },
	];

	const handleSortChange = (selectedOption) => {
		const sortedProducts = [...currentProduct].sort((a, b) => {
			if (selectedOption.value === "delivery") {
				// Сортировка по дате доставки (по возрастанию)
				return new Date(a.delivery) - new Date(b.delivery);
			} else if (
				selectedOption.value === "rating" ||
				selectedOption.value === "reviews_count"
			) {
				// Сортировка по рейтингу или количеству отзывов (по убыванию)
				return b[selectedOption.value] - a[selectedOption.value];
			} else {
				// Сортировка по цене (по возрастанию)
				return a[selectedOption.value] - b[selectedOption.value];
			}
		});

		setCurrentProduct(sortedProducts);
	};

	const buttonSort = (
		<div className={styles.buttonSortConteiner}>
			<span className={styles.buttonSortSpan}>Сортировка</span>
			<Select
				className={styles.Select}
				options={options}
				defaultValue={null}
				onChange={handleSortChange}
			/>
		</div>
	);

	return (
		<main className={styles.container}>
			<div className={styles.header}>
				<Link to="/" className={styles.backButton}>
					<button>НА ГЛАВНУЮ </button>
				</Link>
				<h2 className={styles.pageTitle}>Выбранный товар</h2>
			</div>
			{loadingStatusBasicProduct ? (
				<div className={styles.skeletonWrapper}>
					<Skeleton />
				</div>
			) : (
				<div className={styles.productCardContainer}>
					<ProductCard {...products} />
				</div>
			)}

			<section className={styles.productsSection}>
				<div className={styles.sort}>
					<span className={styles.analog}>Аналогичные товары</span>
					{loadingStatus ? (
						<ClipLoader size={60} color={"#86C232"} />
					) : (
						buttonSort
					)}
				</div>
				{currentProduct && currentProduct.length > 0 ? grid : ""}
			</section>
		</main>
	);
};

export default SecondProductSearch;
