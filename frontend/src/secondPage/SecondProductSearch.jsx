import React from "react";
import { SearchBar } from "../components/SearchBar";
import { ProductGrid } from "../components/ProductGrid";
import styles from "./SecondProductSearch.module.css";
import { ProductCard } from "../components/ProductCard";
import { Link } from "react-router-dom";

const SecondProductSearch = () => {
	return (
		<main className={styles.container}>
			<div className={styles.options}>
				<Link to="/">
					<button>ВЕРНУТЬСЯ НАЗАД</button>
				</Link>
				<ProductCard></ProductCard>

				<input
					id="searchInput"
					type="text"
					className={styles.searchInput}
					placeholder="введите ссылку"
				/>
			</div>
			<section className={styles.productsSection}>
				<ProductGrid />
			</section>
		</main>
	);
};

export default SecondProductSearch;
