import React from "react";
import { ProductCard } from "./ProductCard";
import styles from "./ProductGrid.module.css";

const products = [
	{
		title: "название товара",
		description: "описание товара",
		price: "1000₽",
		deliveryDate: "01.01.2024",
	},
	{
		title: "название товара",
		description: "описание товара",
		price: "2000₽",
		deliveryDate: "02.01.2024",
	},
	{
		title: "название товара",
		description: "описание товара",
		price: "3000₽",
		deliveryDate: "03.01.2024",
	},
];

export const ProductGrid = () => {
	return (
		<div className={styles.productGrid}>
			{products.map((product, index) => (
				<ProductCard key={index} {...product} />
			))}
		</div>
	);
};
