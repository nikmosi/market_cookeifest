import React, { useState } from "react";
import { SearchBar } from "../components/SearchBar";
import { ProductGrid } from "../components/ProductGrid";
import styles from "./ProductSearch.module.css";

const MainProductSearch = () => {
	const [component, setComponent] = useState(null);
	return (
		<main className={styles.container}>
			<h1 className={styles.title}>сайтик МКЛП</h1>
			<SearchBar />
			<section className={styles.productsSection}>
				<ProductGrid />
			</section>
		</main>
	);
};

export default MainProductSearch;
