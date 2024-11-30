import React from "react";
import styles from "./ListProductCard.module.css";
import { addProductId } from "../API/localStorageUtils";
import { useNavigate } from "react-router-dom";

const ListProductCard = ({ id, name, description, price, delivery, rating, reviews_count, images, type = "analog" }) => {
  const navigate = useNavigate();
  const handleSearch = () => {
    const article = id;
    if (article) {
      addProductId(article);

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
    <>
      <article className={styles.productCard}>
        <div className={styles.imageContainer}>
          {images && images.length > 0 ? (
            <img src={images[0]} alt={name} className={styles.productImage} />
          ) : (
            <div className={styles.placeholderImage}>Изображение отсутствует</div>
          )}
        </div>
        <div className={styles.imgdescription}>
          <h2 className={styles.productTitle}>{name || "Название отсутствует"}</h2>

          <div className={styles.productDetails}>
            <p className={styles.priceDelivery}>
              <strong>Цена:</strong> {price ? `${price} ₽` : "Не указана"}
              <br />
              <strong>Доставка:</strong> {delivery || "Неизвестно"}
            </p>

            {rating && reviews_count && (
              <p className={styles.ratingReviews}>
                <strong>Рейтинг:</strong> {rating} ⭐
                <br />
                <strong>Отзывы:</strong> {reviews_count}
              </p>
            )}
          </div>
          <div className={styles.buttons}>
            <button
              className={styles.actionButton}
              onClick={() => window.open(`https://www.wildberries.ru/catalog/${id}/detail.aspx`, "_blank")}
            >
              Открыть
            </button>
            {type === "history" && (
              <button className={styles.searchButton} onClick={handleSearch}>
                Поиск
              </button>
            )}
          </div>
        </div>
      </article>
    </>
  );
};

export default ListProductCard;
