import React from "react";
import styles from "./ProductCard.module.css";
import { Link } from "react-router-dom";

export const ProductCard = ({
	id,
	name,
	description,
	price,
	delivery,
	rating,
	reviews_count,
	images,
}) => {
	return (
		<>
			<article className={styles.productCard}>
				{/* Блок изображения, используем первое изображение из массива */}
				<div className={styles.imageContainer}>
					{images && images.length > 0 ? (
						<img src={images[0]} alt={name} className={styles.productImage} />
					) : (
						<div className={styles.placeholderImage}>
							Изображение отсутствует
						</div>
					)}
				</div>
				<div className={styles.imgdescription}>
					{/* Название товара */}
					<h2 className={styles.productTitle}>
						{name || "Название отсутствует"}
					</h2>

					{/* Описание товара */}
					<p className={styles.productDescription}>
						{description || "Описание отсутствует"}
					</p>

					{/* Детали товара */}
					<div className={styles.productDetails}>
						<p className={styles.priceDelivery}>
							<strong>Цена:</strong> {price ? `${price} ₽` : "Не указана"}
							<br />
							<strong>Доставка:</strong> {delivery || "Неизвестно"}
						</p>

						{/* Рейтинг и количество отзывов */}
						{rating && reviews_count && (
							<p className={styles.ratingReviews}>
								<strong>Рейтинг:</strong> {rating} ⭐
								<br />
								<strong>Отзывы:</strong> {reviews_count}
							</p>
						)}
					</div>
					{/* Кнопка действия */}
					<button
						className={styles.actionButton}
						onClick={() =>
							window.open(
								`https://www.wildberries.ru/catalog/${id}/detail.aspx`,
								"_blank"
							)
						}
					>
						Перейти
					</button>
				</div>
			</article>
		</>
	);
};
