import React from "react";
import styles from "./SearchBar.module.css";
import { useNavigate } from "react-router-dom";
import extractId from "../controllers/extractId";
import { addProductId } from "../API/localStorageUtils";

export const SearchBar = () => {
	const [searchLink, setSearchLink] = React.useState("");
	const navigate = useNavigate();

	const onButtonClick = () => {
		const article = extractId(searchLink);
		if (article) {
			// Добавляем ID в localStorage
			addProductId(article);

			// Проверяем, был ли ID сохранен
			const storedIds = JSON.parse(localStorage.getItem("productIds")) || [];
			if (storedIds.includes(article)) {
				navigate("/resault"); // Перенаправление на другую страницу
			} else {
				alert("Не удалось сохранить ID. Попробуйте еще раз.");
			}
		} else {
			alert("Некорректная ссылка. Проверьте URL.");
		}
	};

	return (
		<form
			className={styles.searchContainer}
			onSubmit={(e) => e.preventDefault()}
		>
			<label htmlFor="searchInput" className={styles.visuallyHidden}>
				введите ссылку
			</label>
			<input
				id="searchInput"
				type="text"
				className={styles.searchInput}
				placeholder="введите ссылку"
				onChange={(e) => setSearchLink(e.target.value)}
			/>
			<button
				type="submit"
				className={styles.searchButton}
				onClick={onButtonClick}
			>
				найти
			</button>
		</form>
	);
};

// export default function BookingsList({ onComponentSelect }) {
// 	return (
// 		<div className={styles.bookingsColumn}>
// 			<nav className={styles.bookingsList}>
// 				<Link onClick={() => onComponentSelect(<UserInfo />)}>
// 					<h2 className={styles.sectionTitle}>Данные</h2>
// 				</Link>
// 				<Link onClick={() => onComponentSelect(<DoneBooking />)}>
// 					<div className={styles.activeBookings}>Завершённые брони</div>
// 				</Link>
// 				<Link onClick={() => onComponentSelect(<ActivBooking />)}>
// 					<div className={styles.activeBookings}>Активные брони</div>
// 				</Link>
// 				<div className={styles.activeBookings}>Турниры</div>
// 			</nav>
// 		</div>
// 	);
// }
